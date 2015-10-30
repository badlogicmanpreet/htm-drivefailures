SWARM_DESCRIPTION = {
    "includedFields": [
        {
            "fieldName": "GList1",
            "fieldType": "float"
        },
        {
            "fieldName": "PList",
            "fieldType": "float"
        },
        {
            "fieldName": "Servo1",
            "fieldType": "float"
        },
        {
            "fieldName": "Servo2",
            "fieldType": "float"
        },
        {
            "fieldName": "Servo3",
            "fieldType": "float"
        },
        {
            "fieldName": "Servo5",
            "fieldType": "float"
        },
        {
            "fieldName": "ReadError1",
            "fieldType": "float"
        },
        {
            "fieldName": "ReadError2",
            "fieldType": "float"
        },
        {
            "fieldName": "ReadError3",
            "fieldType": "float"
        },
        {
            "fieldName": "FlyHeight5",
            "fieldType": "float"
        },
        {
            "fieldName": "FlyHeight6",
            "fieldType": "float"
        },
        {
            "fieldName": "FlyHeight7",
            "fieldType": "float"
        },
        {
            "fieldName": "FlyHeight8",
            "fieldType": "float"
        },
        {
            "fieldName": "FlyHeight9",
            "fieldType": "float"
        },
        {
            "fieldName": "FlyHeight10",
            "fieldType": "float"
        },
        {
            "fieldName": "FlyHeight11",
            "fieldType": "float"
        },
        {
            "fieldName": "FlyHeight12",
            "fieldType": "float"
        },
        {
            "fieldName": "ReadError18",
            "fieldType": "float"
        },
        {
            "fieldName": "ReadError19",
            "fieldType": "float"
        },
        {
            "fieldName": "Servo7",
            "fieldType": "float"
        },
        {
            "fieldName": "Servo8",
            "fieldType": "float"
        },
        {
            "fieldName": "ReadError20",
            "fieldType": "float"
        },
        {
            "fieldName": "GList2",
            "fieldType": "float"
        },
        {
            "fieldName": "GList3",
            "fieldType": "float"
        },
        {
            "fieldName": "Servo10",
            "fieldType": "float"
        },
        {
            "fieldName": "class",
            "fieldType": "string"
        }
    ],
    "streamDef": {
        "info": "hardrive",
        "version": 1,
        "streams": [
            {
                "info": "harddrive-smart-data-pp-to-train.csv",
                "source": "file://harddrive-smart-data-pp-to-train.csv",
                "columns": [
                    "*"
                ]
            }
        ]
    },
    "inferenceType": "TemporalMultiStep",
    "inferenceArgs": {
        "predictionSteps": [
            1
        ],
        "predictedField": "class"
    },
    "iterationCount": 10,
    "swarmSize": "small"
}