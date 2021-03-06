CREATE TABLE auto2.t_race_head (
    dated date,
    place character varying(10),
    round smallint,
    race_name character varying(100) NOT NULL,
    distance integer NOT NULL,
    weather character varying(10) NOT NULL,
    temperature smallint NOT NULL,
    humidity smallint NOT NULL,
    runway_temperature smallint NOT NULL,
    runway_condition character varying(10) NOT NULL,
    race_system character varying(10) NOT NULL,
    race_type character varying(10) NOT NULL,
    PRIMARY KEY (dated, place, round)
);
