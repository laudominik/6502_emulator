    .org $8000
start:

    tsx
    stx $00
    stx $4000

    inc $4000

    ldy $00
    sty $01
    sty $4001

    .org $FFFC
    .word start
    .word $0000
