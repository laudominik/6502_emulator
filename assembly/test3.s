    .org $8000
start:
    lda #64
    sta $4000
    lda #4
    ora $4000
    asl $4000
    asl $4000
    asl $4000

    php

    .org $FFFC
    .word start
    .word $0000
