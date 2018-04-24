create table user(
    id bigint(20) unsigned not null primary key auto_increment,
    name varchar(32) not null unique,
    description text not null default '',
    mtime timestamp not null default current_timestamp on update current_timestamp,
    ctime timestamp not null default current_timestamp
)ENGINE=InnoDB default charset=utf8mb4;
