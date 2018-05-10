CREATE TABLE `db_record` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `title` varchar(255) NOT NULL DEFAULT '',
      `comment` text NOT NULL,
      `url` varchar(255) NOT NULL DEFAULT '',
      `pub` varchar(255) NOT NULL DEFAULT '',
      `mark_date` timestamp NOT NULL,
      `tags` varchar(255) NOT NULL DEFAULT '',
      `rating` tinyint NOT NULL DEFAULT 0,
      PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
