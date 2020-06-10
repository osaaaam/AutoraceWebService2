CREATE TABLE auto2.t_race_payoff (
    dated date,
    place character varying(10),
    round smallint,
    payoff_3t bigint NOT NULL,
    payoff_3f bigint NOT NULL,
    payoff_2t bigint NOT NULL,
    payoff_2f bigint NOT NULL,
    payoff_1t bigint NOT NULL,
    first_place smallint NOT NULL,
    second_place smallint NOT NULL,
    third_place smallint NOT NULL,
    fourth_place smallint NOT NULL,
    fifth_place smallint NOT NULL,
    sixth_place smallint NOT NULL,
    seventh_place smallint NOT NULL,
    eighth_place smallint,
    PRIMARY KEY (dated, place, round)
);
