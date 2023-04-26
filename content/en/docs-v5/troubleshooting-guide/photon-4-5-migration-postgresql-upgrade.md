---
title:  Photon 4.0 to Photon 5.0 Migration and PostgreSQL Upgrade
weight: 11
---

We assume that PostgreSQL v10, v13,  or v14 is installed in Photon OS 4.0 before the upgrade. This leads to multiple scenarios during Photon OS 4.0 to Photon OS 5.0 upgrade as follows:


- PostgreSQL (v10 in Ph4) → PostgreSQL (v13/v14/v15 in Ph5) - This is not supported using `pg_upgrade`, user has to take a `pg_dump` of the DB and do a `pg_restore` after the upgrade as PostgreSQL 10 is EOL in 2022. It is recommended that you migrate to PostgreSQL v13 or v14 in Photon OS 4.0 before migrating to Photon OS 5.0. PostgreSQL 10's sole purpose is to help migrate from Photon OS 3.0 to Photon OS 4.0, and to convert PostgreSQL DB to a higher and supported version of PostgreSQL.

- PostgreSQL (v13 in Photon OS 4.0) → PostgreSQL (v13/v14/v15 in Photon 5.0)
- PostgreSQL (v14 in Photon OS 4.0) → PostgreSQL (v14/v15 in Photon OS 5.0)


Assuming that you use PostgreSQL v13 or a higher version in Photon OS 4.0, PostgreSQL is upgraded to the same version in Photon OS 5.0.

If you need a higher version of PostgreSQL, install the available newer version manually and migrate the DB with caution.

By default, PostgreSQL binaries and libraries point to the most recent version of PostgreSQL available in the system.

Note that it is possible to install and use multiple versions of PostgreSQL at the same time in Photon OS. For example, if you have v13, v14, v15 of PostgreSQL installed altogether, by default, the binaries and libraries used are from PostgreSQL v15.

Perform the following steps to keep using a lower version of PostgreSQL when you have a higher version of PostgreSQL installed in the same system.

**PostgreSQL (v13 in Photon 4.0) → PostgreSQL (v13/v14/v15 in Photon 5.0)**

In this case, we need to install postgresql v13 in Photon  OS 5.0 manually, and then migrate DB to PostgreSQL v14 or PostgreSQL v15 or keep using PostgreSQL v13.

To keep using PostgreSQL v13 in Photon OS 5.0, execute the following command:
```
$ sudo tdnf install -y postgresql13
```   
Set PATH & LD_LIBRARY_PATH to the right locations to keep using PostgreSQL v13.

```
$ export PATH=/usr/pgsql/13/bin:$PATH
```   
```
$ export LD_LIBRARY_PATH=/usr/pgsql/13/lib:$LD_LIBRARY_PATH
```   

To migrate to PostgreSQL v14 or PostgreSQL v15, execute the following commands:

```
$ initdb -D <pgsql14/pgsql15-data-dir>
```    
```
$ pg_upgrade --old-datadir <pgsql13-data-dir> --new-datadir <pgsql14/pgsql15-data-dir> --old-bindir /usr/pgsql/13/bin/ --new-bindir /usr/bin
```    

**PostgreSQL (v14 in Photon 4.0) → PostgreSQL (v14/v15 in Photon 5.0)**

In this case, we need to install PostgreSQL v13 in Photon 5.0 manually, and then migrate DB to PostgreSQL v15 or keep using PostgreSQL v14.

To keep using PostgreSQL v14 in Photon 5.0, execute the following command:

```
$ sudo tdnf install -y postgresql14
```    
Set PATH & LD_LIBRARY_PATH to right locations to keep using PostgreSQL v14.

```
$ export PATH=/usr/pgsql/14/bin:$PATH
```   
```
$ export LD_LIBRARY_PATH=/usr/pgsql/14/lib:$LD_LIBRARY_PATH
```   


To migrate to PostgreSQL v14 or PostgreSQL v15, execute the following commands:

```
$ initdb -D <pgsql15-data-dir>
```    
```
$ pg_upgrade --old-datadir <pgsql14-data-dir> --new-datadir <pgsql15-data-dir> --old-bindir /usr/pgsql/14/bin/ --new-bindir /usr/bin
```   

**Note**: If you chose the `pg_upgrade` method, you can remove the older version of PostgreSQL once DB is migrated.
Do not forget to take a backup of your DB data, and take VM snapshot before making changes to DB or your VM.