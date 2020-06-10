create table auto2.t_race_info (
  dated date not null
  , place character varying(10) not null
  , round smallint not null
  , car_no smallint not null
  , racer character varying(20) not null
  , represent character varying(20) not null
  , hande smallint not null
  , trialrun real not null
  , deviation real not null
  , position_x smallint not null
  , position_y smallint not null
  , primary key (dated,place,round,car_no)
);
