CREATE TABLE public.replay
(
    id serial NOT NULL,
    map text NOT NULL,
    game_type text NOT NULL,
    winner integer,
    ban1 text,
    ban2 text,
    ban3 text,
    ban4 text,
    ban5 text,
    ban6 text,
    pick1 text NOT NULL,
    pick2 text NOT NULL,
    pick3 text NOT NULL,
    pick4 text NOT NULL,
    pick5 text NOT NULL,
    pick6 text NOT NULL,
    pick7 text NOT NULL,
    pick8 text NOT NULL,
    pick9 text NOT NULL,
    pick10 text NOT NULL,
    level1 integer NOT NULL,
    level2 integer NOT NULL,
    level3 integer NOT NULL,
    level4 integer NOT NULL,
    level5 integer NOT NULL,
    level6 integer NOT NULL,
    level7 integer NOT NULL,
    level8 integer NOT NULL,
    level9 integer NOT NULL,
    level10 integer NOT NULL,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.replay
    OWNER to hotsy;