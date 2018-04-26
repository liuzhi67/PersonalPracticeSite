create table user(
    id bigint(20) unsigned not null primary key auto_increment,
    site_id bigint(20) unsigned not null comment 'site.id',
    user_id varchar(32) not null unique,
    name varchar(128) not null unique,
    description text not null default '',
    mtime timestamp not null default current_timestamp on update current_timestamp,
    ctime timestamp not null default current_timestamp
)ENGINE=InnoDB default charset=utf8mb4 comment '配置用户表';
