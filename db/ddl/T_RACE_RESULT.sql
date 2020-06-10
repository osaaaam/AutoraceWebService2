create table auto2.t_race_result (
  dated date not null
  , place character varying(10) not null
  , round smallint not null
  , car_no smallint not null
  , racetime real not null
  , starttime real not null
  , rank smallint not null
  , primary key (dated,place,round,car_no)
);
