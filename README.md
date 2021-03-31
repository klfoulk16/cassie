# Meet Cassie, an baby SSTable Database

Cassie was born out of a desire to do more than just read Designing Data Intensive Applications, but rather to see it live in code. For most of coding career I've worked with Postgres and SQLite, but never really understood what was going on under the hood. While I know that those two databases use B-trees, the SSTable and LSM-tree model seemed much more intrigueing hence I'll be building my database using that structure. Let's get started!

## Version 1

This project will likely have many iterations as I add more and more layers of complexity. While I have mapped out my goals in /Cassie, I plan to focus on creating an even simpler in-memory hard-coded database in /babyCassie that consists of one table and is able to successfully perform reads/writes/deletions and works with my Cassiequill query language. You must slay the baby dragons before you attempt the real one.

### Notes:

#### CassQL Restrictions:

1. -1 and floats are not counted as numeric. In fact floats will be seperated into 3 segments and periods currently aren't recognized.
2. Commas optional after items for INSERT INTO table (column1, column2,) and values

## The Ideal Project

- Memtables using Red Black Trees
- Log File in Case of Crash
- A baby SQL-like query language and REPL
- Writing memtable to disk, including creation of sparse index and compressing blocks.
- Background Compaction and Merging using Mergesort
- Tombstones
- Creation of multiple tables in the database

## Questions

- How should I have the database to run persitently in the background? Could I use docker? 
- Can I create a simple visualization?
- Is there a simple project I can create to demonstrate a use case?
- What will tests look like? (I'll have to figure this one out pretty quickly)