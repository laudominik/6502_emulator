    .org $8000
start:
    lda #$F0
    sta $4000
    lda #$FF
    rol $4000
    and $4000

    .org $FFFC
    .word start
    .word $0000
