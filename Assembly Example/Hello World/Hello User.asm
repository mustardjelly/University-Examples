	.ORIG x3000
	LEA r0, welcome
	PUTS
	LEA r1, name
loop	GETC
	OUT
	ADD r2, r0, #-10	;check for new line
	brz outloop
	STR r0, r1, #0
	ADD r1, r1, #1
	BR loop

outloop	LEA r0, hello
	PUTS
	LEA r0, name
	PUTS
	HALT


welcome .STRINGZ "Please enter your name: "
hello	.STRINGZ "Hello "
name	.BLKW 80
	.end
