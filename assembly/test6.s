    .org $8000
start:

    lda #$FF
    and #$40


    .org $FFFC
    .word start
    .word $0000
