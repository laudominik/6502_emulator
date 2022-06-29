    .org $8000
start:
    lda #4
    sta $05
    lda #64
    and $05


    .org $FFFC
    .word start
    .word $0000
