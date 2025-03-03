create table tb_article (
    id int(11) primary key auto_increment,
    title varchar(255) not null,
    content text not null,
    is_deleted bool not null default false,
    created_at datetime not null default NOW(),
    updated_at datetime not null default NOW(),
    deleted_at datetime
);

create table tb_article_comment(
    id int(11) primary key auto_increment,
    article_id int(11) not null,
    comment_id int(11),
    content text not null,
    level int(11) not null, default 0,
    is_deletd bool not null default false,
    created_at datetime not null default NOW(),
    updated_at datetime not null default NOW(),
    deleted_at datetime,
    foreign key (article_id) references tb_article(id)
);

create table tb_article_tag(
    id int(11) primary key auto_increment,
    article_id int(11),
    tagging varchar(255) not null,
    created_at datetime not null default NOW(),
    updated_at datetime not null default NOW(),
    deleted_at datetime,
    foreign key (article_id) references tb_article(id)
);

create table tb_article_attached_file(
    id int(11) primary key auto_increment,
    article_id int(11),
    s3_bucket_name varchar(255) not null,
    s3_key varchar(255) not null,
    filename varchar(255) not null,
    file_size int(11) not null default 0,
    file_type varchar(255) not null,
    is_deleted bool not null default false,
    created_at datetime not null default NOW(),
    deleted_at datetime,
    foreign key (article_id) references tb_article(id)
);