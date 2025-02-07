CREATE KEYSPACE logKeyspace WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE logKeyspace.log_table(
    host text PRIMARY KEY,
    user_identifier text, 
    datetime text, 
    method text, 
    request text,
    protocol text,
    status text,
    bytes text,
    referer text
);

CREATE TABLE logKeyspace.ipInfo(
    query TEXT PRIMARY KEY,
    status TEXT,
    continent TEXT,
    continentCode TEXT,
    country TEXT,
    countryCode TEXT,
    region TEXT,
    regionName TEXT,
    city TEXT,
    district TEXT,
    zip TEXT,
    lat DOUBLE,
    lon DOUBLE,
    timezone TEXT,
    offset INT,
    currency TEXT,
    isp TEXT,
    org TEXT,
    as TEXT,
    asname TEXT,
    mobile BOOLEAN,
    proxy BOOLEAN,
    hosting BOOLEAN
);

