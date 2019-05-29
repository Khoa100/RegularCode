wizard(ron).
hasWand(harry).
quidditchPlayer(harry).
witch(X) :- hasBroom(X), hasWand(X).
hasBroom(X) :- quidditchPlayer(X).
