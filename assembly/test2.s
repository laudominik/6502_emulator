    .org $8000
start:
    lda #$FF
    sta $4001
    ldx $4001

    lda #$0F
    sta $01
    ldx $01

    .org $FFFC
    .word start
    .word $0000
