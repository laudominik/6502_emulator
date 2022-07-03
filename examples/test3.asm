    .org $8000
start:
    lda #64
    asl

    php

    .org $FFFC
    .word start
    .word $0000
