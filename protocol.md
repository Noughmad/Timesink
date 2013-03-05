# Timesink data protocol

The Timesink data protocol is used to synchronize data between a central server and one or more clients. Timesink does not care how data is stored on either end, but each participant must be able to serialize its data into a compatible format.

There are two ways to transmit data in Timesink. The first is to transfer the complete data set, each field containing a corresponding timestamp. The other is to only send a log of all changes, where every change contains its own timestamp. 
Both modes use JSON to format the data. Detailed description of both modes follow. 

In all cases, the client is the one to initiate the transaction. It sends its data, in one of the two formats, to the server. The server then applies the changes sent by the client, and responds with its own data. 

## Complete data set

In this mode, the client sends it entire data store to the server. This is usually easier to implement on the client side, but is impractical for large datasets. The data is a list of JSON objects. Each object has a "_meta" property, which holds the class name and creation/deletion timestamp. If the object has not been deleted, which will usually be the case, the "deletedAt" entry has to be either empty or omitted. It is important to store information about the deletion time, because the same object may have been modified on the server in the meantime, and the deletion should be cancelled in this case.

The following is an example of a complete dataset of two objects with type "Person" and two fields. The third object, with id of 3, has been deleted by the client. 

    [
      {
        "_meta": {
          "className": "Person",
          "id" : 1
          "createdAt": "2013-03-05-16-05",
          "deletedAt": ""
        },
        "name": {
          value: "John Smith",
          timestamp: "2013-03-05-16-05"
        },
        "age": {
          value: 42,
          timestamp: "2013-03-05-18-16"
        }
      },
      {
        "_meta": {
          "className": "Person",
          "id": 2
          "createdAt": "2013-03-05-18-08",
        },
        "name": {
          value: "Jane Smith",
          timestamp: "2013-03-05-19-48"
        },
        "age": {
          value: 39,
          timestamp: "2013-03-05-19-48"
        }
      },
      {
        "_meta": {
          "className": "Person",
          "id": 3
          "deletedAt": "2013-03-04-12-24"
        }
      }
    ]

## Transaction log

For any non-trivial data set, it is usually more efficient to only send the modification log instead of the entire data. In this case, the client transmits a list of change objects. 

The following example shows a set of changes the describe a creation of a Person object, an update that changes some of its properties, and its deletion. 

    [
      {
        "object": 4,
        "className": "Person"
        "action": "create",
        "properties": [
          "age": 39
          "name": "John Doe"
        ],
        "timestamp": "2013-03-05-20-04"
      },
      {
        "object": 4,
        "action": "update",
        "properties": [
          "age": 40
        ],
        "timestamp": "2013-03-05-21-11"
      },
      {
        "object": 4,
        "action": "delete",
        "timestamp": "2013-03-05-22-00"
      }
    ]
