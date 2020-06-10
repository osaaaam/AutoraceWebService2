CREATE TABLE auto2.m_anaylize_model (
    model_no smallint PRIMARY KEY,
    algorithm character varying(100) NOT NULL,
    algorithm_list character varying(2000),
    features character varying(2000) NOT NULL,
    target character varying(50) NOT NULL
);
