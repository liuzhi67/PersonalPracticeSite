create table site(
    id bigint(20) unsigned not null primary key auto_increment,
    name varchar(32) not null unique,
    url varchar(128) not null unique,
    mtime timestamp not null default current_timestamp on update current_timestamp,
    ctime timestamp not null default current_timestamp
)ENGINE=InnoDB default charset=utf8mb4;
