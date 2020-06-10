CREATE TABLE auto2.w_race_head (
    dated date,
    place character varying(10),
    round smallint,
    race_name character varying(100),
    distance integer,
    weather character varying(10),
    temperature smallint,
    humidity smallint,
    runway_temperature smallint,
    runway_condition character varying(10),
    race_system character varying(10),
    race_type character varying(10),
    PRIMARY KEY (dated, place, round)
);
