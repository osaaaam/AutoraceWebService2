CREATE TABLE auto2.w_anaylize_result_value (
    dated date,
    place character varying(10),
    round smallint,
    model_no smallint,
    first_car real,
    second_car real,
    third_car real,
    fourth_car real,
    fifth_car real,
    sixth_car real,
    seventh_car real,
    eighth_car real,
    PRIMARY KEY (dated, place, round, model_no)
);
