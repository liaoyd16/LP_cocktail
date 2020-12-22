
%% compose2: combine 2 bands into 1 signal
function [x_recover] = compose2(xlow_2, xhigh_2, nfft)
    window_low  = fir1(nfft, 1/2, 'low');
    xlow_0ins  = zeros(2*size(xlow_2, 1), 1);
    xhigh_0ins = zeros(2*size(xhigh_2,1), 1);
    xlow_0ins(1:2:end)  = xlow_2;
    xhigh_0ins(1:2:end) = xhigh_2;
    xlow_ups  = conv(window_low, xlow_0ins);
    xhigh_ups = conv(window_low, xhigh_0ins);
    xhigh_hilb2 = hilbert(xhigh_ups);
    xhigh_shift2 = xhigh_hilb2 .* ((-j) .^ (0:size(xhigh_hilb2,1)-1))';
    xhigh_ih2 = xhigh_shift2 + conj(xhigh_shift2);
    x_recover = xlow_ups + xhigh_ih2;
    x_recover = x_recover(nfft:end-nfft-1);
end
