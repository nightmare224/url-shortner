GRANT ALL PRIVILEGES ON DATABASE postgres TO postgresadmin;
CREATE TABLE url_mapper
(
  url_id INT NOT NULL UNIQUE,
  short_url_id VARCHAR(20) NOT NULL,
  short_base_url VARCHAR(200) NOT NULL,
  full_url VARCHAR(1000) NOT NULL,
  PRIMARY KEY (url_id)
);

INSERT INTO url_mapper VALUES(1,'b','dummy','dummy');