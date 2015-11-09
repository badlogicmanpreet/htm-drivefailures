__author__ = 'manpreet.singh'

import csv
from collections import deque
from abc import ABCMeta, abstractmethod
from nupic.algorithms import anomaly_likelihood
# Try to import matplotlib, but we don't have to.
try:
  import matplotlib
  matplotlib.use('TKAgg')
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
  from matplotlib.dates import date2num, DateFormatter
except ImportError:
  pass

WINDOW = 300
HIGHLIGHT_ALPHA = 0.3
ANOMALY_HIGHLIGHT_COLOR = 'red'
WEEKEND_HIGHLIGHT_COLOR = 'yellow'
ANOMALY_THRESHOLD = 0.9

# plt.ion()
# ydata = [0] * 50
# ax1 = plt.axes()
# line, = plt.plot(ydata)
# plt.ylim(- 1.0, 2)

def plotMe(timestamp, rawData, anomalyScore):

    # plt.xlim(0, 7)
    #
    # #plt.plot(rawData)
    #
    # line.set_xdata(timestamp)
    # line.set_ydata(rawData)  # update the data
    # line.set_ydata(anomalyScore)  # update the data
    #
    # plt.draw()

    print()


def extractAnomalyIndices(anomalyLikelihood):
  anomaliesOut = []
  anomalyStart = None
  for i, likelihood in enumerate(anomalyLikelihood):
    if likelihood >= ANOMALY_THRESHOLD:
      if anomalyStart is None:
        # Mark start of anomaly
        anomalyStart = i
    else:
      if anomalyStart is not None:
        # Mark end of anomaly
        anomaliesOut.append((
          anomalyStart, i, ANOMALY_HIGHLIGHT_COLOR, HIGHLIGHT_ALPHA
        ))
        anomalyStart = None

  # Cap it off if we're still in the middle of an anomaly
  if anomalyStart is not None:
    anomaliesOut.append((
      anomalyStart, len(anomalyLikelihood)-1,
      ANOMALY_HIGHLIGHT_COLOR, HIGHLIGHT_ALPHA
    ))

  return anomaliesOut


class NuPICOutput(object):

  __metaclass__ = ABCMeta


  def __init__(self, name):
    self.name = name
    self.anomalyLikelihoodHelper = anomaly_likelihood.AnomalyLikelihood()


  @abstractmethod
  def write(self, timestamp, value, predicted, anomalyScore):
    pass


  @abstractmethod
  def close(self):
    pass


class NuPICPlotOutput(NuPICOutput):

  def __init__(self, *args, **kwargs):
    super(NuPICPlotOutput, self).__init__(*args, **kwargs)
    # Turn matplotlib interactive mode on.
    plt.ion()
    self.dates = []
    self.convertedDates = []
    self.value = []
    self.allValues = []
    self.predicted = []
    self.anomalyScore = []
    self.anomalyLikelihood = []
    self.actualLine = None
    self.predictedLine = None
    self.anomalyScoreLine = None
    self.anomalyLikelihoodLine = None
    self.linesInitialized = False
    self._chartHighlights = []
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3,  1])

    self._mainGraph = fig.add_subplot(gs[0, 0])
    plt.title(self.name)
    plt.ylabel('Prediction')
    plt.xlabel('Time')

    self._anomalyGraph = fig.add_subplot(gs[1])
    plt.ylabel('Anomaly')
    plt.xlabel('Time')

    # Maximizes window
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.tight_layout()


  def initializeLines(self, timestamp):
    print "initializing %s" % self.name
    anomalyRange = (0.0, 1.0)
    maingraphRange = (-1.0, 2.0)
    self.dates = deque([timestamp] * WINDOW, maxlen=WINDOW)
    self.convertedDates = deque(
      [date2num(date) for date in self.dates], maxlen=WINDOW
    )
    self.value = deque([0.0] * WINDOW, maxlen=WINDOW)
    self.predicted = deque([0.0] * WINDOW, maxlen=WINDOW)
    self.anomalyScore = deque([0.0] * WINDOW, maxlen=WINDOW)
    self.anomalyLikelihood = deque([0.0] * WINDOW, maxlen=WINDOW)

    actualPlot, = self._mainGraph.plot(self.dates, self.value)
    actualPlot.axes.set_ylim(maingraphRange)
    self.actualLine = actualPlot
    predictedPlot, = self._mainGraph.plot(self.dates, self.predicted)
    predictedPlot.axes.set_ylim(maingraphRange)
    self.predictedLine = predictedPlot
    self._mainGraph.legend(tuple(['actual', 'predicted']), loc=3)

    anomalyScorePlot, = self._anomalyGraph.plot(
      self.dates, self.anomalyScore, 'm'
    )
    anomalyScorePlot.axes.set_ylim(anomalyRange)

    self.anomalyScoreLine = anomalyScorePlot
    anomalyLikelihoodPlot, = self._anomalyGraph.plot(
      self.dates, self.anomalyScore, 'r'
    )
    anomalyLikelihoodPlot.axes.set_ylim(anomalyRange)
    self.anomalyLikelihoodLine = anomalyLikelihoodPlot
    self._anomalyGraph.legend(
      tuple(['anomaly score', 'anomaly likelihood']), loc=3
    )

    dateFormatter = DateFormatter('%m/%d %H:%M')
    self._mainGraph.xaxis.set_major_formatter(dateFormatter)
    self._anomalyGraph.xaxis.set_major_formatter(dateFormatter)

    self._mainGraph.relim()
    self._mainGraph.autoscale_view(True, True, True)

    self.linesInitialized = True


  def highlightChart(self, highlights, chart):
    for highlight in highlights:
      # Each highlight contains [start-index, stop-index, color, alpha]
      self._chartHighlights.append(chart.axvspan(
        self.convertedDates[highlight[0]], self.convertedDates[highlight[1]],
        color=highlight[2], alpha=highlight[3]
      ))


  def write(self, timestamp, value, predicted, anomalyScore):
      if not self.linesInitialized:
          self.initializeLines(timestamp)

      anomalyLikelihood = self.anomalyLikelihoodHelper.anomalyProbability(
      value, anomalyScore
      )

      self.dates.append(timestamp)
      self.convertedDates.append(date2num(timestamp))
      self.value.append(value)
      self.allValues.append(value)
      self.predicted.append(predicted)
      self.anomalyScore.append(anomalyScore)
      self.anomalyLikelihood.append(anomalyLikelihood)

      # Update main chart data
      self.actualLine.set_xdata(self.convertedDates)
      self.actualLine.set_ydata(self.value)
      self.predictedLine.set_xdata(self.convertedDates)
      self.predictedLine.set_ydata(self.predicted)
      # Update anomaly chart data
      self.anomalyScoreLine.set_xdata(self.convertedDates)
      self.anomalyScoreLine.set_ydata(self.anomalyScore)
      self.anomalyLikelihoodLine.set_xdata(self.convertedDates)
      self.anomalyLikelihoodLine.set_ydata(self.anomalyLikelihood)

      # Remove previous highlighted regions
      for poly in self._chartHighlights:
          poly.remove()
      self._chartHighlights = []

      anomalies = extractAnomalyIndices(self.anomalyLikelihood)

      # Highlight anomalies in anomaly chart
      self.highlightChart(anomalies, self._anomalyGraph)

      maxValue = max(self.allValues)
      self._mainGraph.relim()
      self._mainGraph.axes.set_ylim(0, maxValue + (maxValue * 0.02))
      #self._mainGraph.axes.set_ylim(-1, 2)

      self._mainGraph.relim()
      self._mainGraph.autoscale_view(True, scaley=False)
      self._anomalyGraph.relim()
      self._anomalyGraph.autoscale_view(True, True, True)

      plt.draw()


  def close(self):
    plt.ioff()
    plt.show()


NuPICOutput.register(NuPICPlotOutput)
