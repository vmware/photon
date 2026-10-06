SECTIONS
{
  /* do not allow linker to shrink .rodata.str1.1  */
  .rodata         : { *(.rodata .rodata.* .gnu.linkonce.r.*) }
}

