    .org $8000
start:
    lda #4
    sta $05
    lda #64
    ora $05
    asl

    .org $FFFC
    .word start
    .word $0000
