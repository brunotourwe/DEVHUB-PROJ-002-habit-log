CREATE TABLE daily_log (
    date                DATE        PRIMARY KEY,
    walked              BOOLEAN     NOT NULL,
    no_alcohol_after_21 BOOLEAN     NOT NULL,
    food_respected      BOOLEAN     NOT NULL,
    note                TEXT        NULL,
    special_occasion    BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMP   NOT NULL,
    updated_at          TIMESTAMP   NOT NULL
);

CREATE TABLE weekly_weight (
    year                INTEGER     NOT NULL,
    week                INTEGER     NOT NULL,
    weight_kg           REAL        NOT NULL,
    created_at          TIMESTAMP   NOT NULL,
    PRIMARY KEY (year, week)
);

CREATE TABLE schema_meta (
    version             INTEGER     PRIMARY KEY,
    applied_at          TIMESTAMP   NOT NULL
);
