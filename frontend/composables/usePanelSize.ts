export const usePaneSize = () => {
  const leftWidth = useCookie<number>('left_width', { sameSite: 'lax' });
  const rightTopHeight = useCookie<number>('right_top_height', { sameSite: 'lax' });

  if (!leftWidth.value) leftWidth.value = 400;
  if (!rightTopHeight.value) rightTopHeight.value = 300;

  return {
    leftWidth,
    rightTopHeight,
  };
};
