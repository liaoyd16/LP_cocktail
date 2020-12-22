
%% decompose2: decompose 1 signal into low/high bands, each pi/2
function [xlow_2, xhigh_2] = decompose2(x,nfft)
    window_low  = fir1(nfft, 1/2, 'low');
    window_high = fir1(nfft, 1/2, 'high');
    xlow  = conv(x, window_low);
    xhigh = conv(x, window_high);
    xhigh_hilb = hilbert(xhigh);
    xhigh_shift = xhigh_hilb .* (j.^(0 : size(xhigh_hilb,1)-1))';
    xhigh_ih = xhigh_shift/2 + conj(xhigh_shift)/2;
    xlow_2  = xlow(1:2:end);
    xhigh_2 = xhigh_ih(1:2:end);
end
