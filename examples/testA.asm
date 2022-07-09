    .org $8000
start:
    lda #10
    sta $00

    lsr $00
    lsr

    sta $4000
    lsr $4000

    .org $FFFC
    .word start
    .word $0000
