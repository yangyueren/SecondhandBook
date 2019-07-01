create table book(
book_id int  primary key AUTO_INCREMENT,
isbn varchar(64) not null,
book_name varchar(64) not null,
author varchar(64) not null,
publisher varchar(64) not null,
publish_date varchar(64) not null,
content varchar(512) not null,
picture_url varchar(64) not null,
ini_price float not null,
sell_price float not null
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

create table user(
user_id int  primary key AUTO_INCREMENT,
name varchar(64) not null,
password varchar(64) not null,
email varchar(64) not null,
address varchar(64) not null,
phone varchar(64) not null,
paypal varchar(512) not null,
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

create table orders(
book_id int  primary key AUTO_INCREMENT,
isbn varchar(64) not null,
book_name varchar(64) not null,
author varchar(64) not null,
publisher varchar(64) not null,
publish_date varchar(64) not null,
content varchar(512) not null,
picture_url varchar(64) not null,
ini_price float not null,
sell_price float not null
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

create table book(
book_id int  primary key AUTO_INCREMENT,
isbn varchar(64) not null,
book_name varchar(64) not null,
author varchar(64) not null,
publisher varchar(64) not null,
publish_date varchar(64) not null,
content varchar(512) not null,
picture_url varchar(64) not null,
ini_price float not null,
sell_price float not null
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

create table book(
book_id int  primary key AUTO_INCREMENT,
isbn varchar(64) not null,
book_name varchar(64) not null,
author varchar(64) not null,
publisher varchar(64) not null,
publish_date varchar(64) not null,
content varchar(512) not null,
picture_url varchar(64) not null,
ini_price float not null,
sell_price float not null
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

ALTER TABLE `seek_book` DEFAULT CHARACTER SET utf8;
ALTER TABLE `contact` DEFAULT CHARACTER SET utf8;
ALTER TABLE `orders` DEFAULT CHARACTER SET utf8;
ALTER TABLE `sell_book` DEFAULT CHARACTER SET utf8;
ALTER TABLE `book` DEFAULT CHARACTER SET utf8;
ALTER TABLE `user` DEFAULT CHARACTER SET utf8;
