    .org $8000
start:
    lda #69
    sta $05
    asl $05

    .org $FFFC
    .word start
    .word $0000
