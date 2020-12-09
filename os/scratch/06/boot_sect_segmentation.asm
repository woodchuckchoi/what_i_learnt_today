mov ah, 0x0e ; tty

mov al, [the_secret] ; rubbish
int 0x10

mov bx, 0x7c0 ; segment automatically shifts 4bits (1 place in hex)
mov ds, bx
mov al, [the_secret]
int 0x10

mov al, [es:the_secret] ; rubbish
int 0x10

mov bx, 0x7c0
mov es, bx
mov al, [es:the_secret]
int 0x10

the_secret:
	db "X"

times 510 - ($-$$) db 0
dw 0xaa55
