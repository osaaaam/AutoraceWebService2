CREATE TABLE auto2.t_monthly_log (
    dated date not null,
    place character varying(10) not null,
    round smallint not null,
    status smallint not null,
    err_msg character varying(2000),
    PRIMARY KEY (dated, place, round)
);
