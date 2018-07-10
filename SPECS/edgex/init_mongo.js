//###############################################################################
//# Copyright 2016-2017 Dell Inc.
//#
//# Licensed under the Apache License, Version 2.0 (the "License");
//# you may not use this file except in compliance with the License.
//# You may obtain a copy of the License at
//#
//# http://www.apache.org/licenses/LICENSE-2.0
//#
//# Unless required by applicable law or agreed to in writing, software
//# distributed under the License is distributed on an "AS IS" BASIS,
//# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//# See the License for the specific language governing permissions and
//# limitations under the License.
//#
//###############################################################################
//EdgeX Mongo DB initialization script
//version 1
//author:  Jim White
//Create user for security service in Mongo
db=db.getSiblingDB('admin')
db=db.getSiblingDB('authorization')
db.createUser({ user: "admin",pwd: "password",roles: [ { role: "readWrite", db: "authorization" } ]});
//Create keystore collection
db.createCollection("keyStore");
db.keyStore.insert( { xDellAuthKey: "x-dell-auth-key", secretKey: "EDGEX_SECRET_KEY" } );
//Create Service Mapping
db.createCollection("serviceMapping");
db.serviceMapping.insert( { serviceName: "coredata", serviceUrl: "http://localhost:48080/" });
db.serviceMapping.insert( { serviceName: "metadata", serviceUrl: "http://localhost:48081/" });
db.serviceMapping.insert( { serviceName: "command", serviceUrl: "http://localhost:48082/" });
db.serviceMapping.insert( { serviceName: "rules", serviceUrl: "http://localhost:48084/" });
db.serviceMapping.insert( { serviceName: "notifications", serviceUrl: "http://localhost:48060/" });
db.serviceMapping.insert( { serviceName: "logging", serviceUrl: "http://localhost:48061/" });

db=db.getSiblingDB('admin')
db.system.users.remove({});
db.system.version.remove({});
db.system.version.insert({ "_id" : "authSchema", "currentVersion" : 3 });
db=db.getSiblingDB('admin')
db.createUser({ user: "admin",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "admin" }
  ]
});

db=db.getSiblingDB('metadata')
db.createUser({ user: "meta",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "metadata" }
  ]
});
db.createCollection("addressable");
db.addressable.createIndex({name: 1}, {unique: true});
db.createCollection("command");
db.createCollection("device");
db.device.createIndex({name: 1}, {unique: true});
db.createCollection("deviceProfile");
db.deviceProfile.createIndex({name: 1}, {unique: true});
db.createCollection("deviceReport");
db.deviceReport.createIndex({name: 1}, {unique: true});
db.createCollection("deviceService");
db.deviceService.createIndex({name: 1}, {unique: true});
db.createCollection("provisionWatcher");
db.provisionWatcher.createIndex({name: 1}, {unique: true});
db.createCollection("schedule");
db.schedule.createIndex({name: 1}, {unique: true});
db.createCollection("scheduleEvent");
db.scheduleEvent.createIndex({name: 1}, {unique: true});

db=db.getSiblingDB('coredata')
db.createUser({ user: "core",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "coredata" }
  ]
});
db.createCollection("event");
db.createCollection("reading");
db.createCollection("valueDescriptor");
db.valueDescriptor.createIndex({name: 1}, {unique: true});

db=db.getSiblingDB('rules_engine_db')
db.createUser({ user: "rules_engine_user",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "rules_engine_db" }
  ]
});

db=db.getSiblingDB('notifications')
db.createUser({ user: "notifications",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "notifications" }
  ]
});
db.createCollection("notification");
db.createCollection("transmission");
db.createCollection("subscription");
db.notification.createIndex({slug: 1}, {unique: true});
db.subscription.createIndex({slug: 1}, {unique: true});

db=db.getSiblingDB('logging')
db.createUser({ user: "logging",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "logging" }
  ]
});
db.createCollection("logEntry");
