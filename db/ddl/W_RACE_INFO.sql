create table auto2.w_race_info (
  dated date
  , place character varying(10)
  , round smallint
  , car_no smallint
  , racer character varying(20)
  , represent character varying(20)
  , hande smallint
  , trialrun real
  , deviation real
  , position_x smallint
  , position_y smallint
  , primary key (dated,place,round,car_no)
);
