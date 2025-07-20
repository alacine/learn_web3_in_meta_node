SET NAMES utf8mb4;

ALTER DATABASE practice_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- q1
create table practice_db.student (
    id int not null auto_increment,
    name varchar(255),
    age int not null,
    grade varchar(255),
    PRIMARY KEY(id)
) Engine=InnoDB
  auto_increment=1
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- q2
create table practice_db.accounts (
    id int not null auto_increment,
    balance decimal(10,2) not null default 0,
    PRIMARY KEY(id)
) Engine=InnoDB auto_increment=1
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

create table practice_db.transactions (
    id int not null auto_increment,
    from_account_id int not null default 0,
    to_account_id int not null default 0,
    amount decimal(10, 2) not null default 0,
    PRIMARY KEY(id)
) Engine=InnoDB auto_increment=1
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- sqlx q1
create table practice_db.employees (
    id int not null auto_increment,
    name varchar(255),
    department varchar(255),
    salary decimal(10, 2) not null default 0,
    PRIMARY KEY(id)
) Engine=InnoDB
  auto_increment=1
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

insert into employees(name, department, salary) values("a", "技术部", 10000);
insert into employees(name, department, salary) values("b", "技术部", 20000);
insert into employees(name, department, salary) values("c", "技术部", 15000);
insert into employees(name, department, salary) values("d", "技术部", 16000);
insert into employees(name, department, salary) values("e", "财务部", 13000);
insert into employees(name, department, salary) values("f", "财务部", 14000);

create table practice_db.books (
    id int not null auto_increment,
    title varchar(255),
    author varchar(255),
    price decimal(10, 2) not null default 0,
    PRIMARY KEY(id)
) Engine=InnoDB auto_increment=1
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

insert into books(title, author, price) values("三体", "刘慈欣", 45.50);
insert into books(title, author, price) values("活着", "余华", 32.80);
insert into books(title, author, price) values("围城", "钱钟书", 28.90);
insert into books(title, author, price) values("红楼梦", "曹雪芹", 68.00);
insert into books(title, author, price) values("西游记", "吴承恩", 52.30);
insert into books(title, author, price) values("水浒传", "施耐庵", 48.60);
insert into books(title, author, price) values("三国演义", "罗贯中", 55.20);
insert into books(title, author, price) values("平凡的世界", "路遥", 42.70);
insert into books(title, author, price) values("白鹿原", "陈忠实", 38.90);
insert into books(title, author, price) values("百年孤独", "加西亚·马尔克斯", 41.50);
