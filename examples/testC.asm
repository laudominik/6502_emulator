    .org $8000
start:

    lda #00
    cmp #00
    php
    tsx
    txa
    tay

    .org $FFFC
    .word start
    .word $0000
