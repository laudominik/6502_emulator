    .org $8000
start:

    lda #$ff
    ror
    ror

    .org $FFFC
    .word start
    .word $0000
