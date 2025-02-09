CREATE SCHEMA real_time_logs;
CREATE SCHEMA batch_logs;

CREATE TABLE real_time_logs.status_per_window(
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    status_group VARCHAR,
    request_status_count INTEGER
);

CREATE TABLE real_time_logs.protocol_per_window(
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    protocol VARCHAR,
    request_protocol_count INTEGER
);

CREATE TABLE real_time_logs.method_per_window(
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    method VARCHAR,
    request_method_count INTEGER
);

CREATE TABLE batch_logs.host_informations(
    host VARCHAR,
    time_stamp TIMESTAMP,
    proxy VARCHAR,
    country VARCHAR,
    isp VARCHAR,
    org VARCHAR
);

-- DROP TABLE batch_logs.host_informations; 
SELECT * FROM batch_logs.host_informations;
