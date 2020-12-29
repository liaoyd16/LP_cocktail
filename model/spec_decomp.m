
%% spec_recomb: function description
function [an_1] = spec_decomp(an) % an = [1, az^-1, az^-2, ...]
    Nregress = length(an) - 1;
    Hz = tf([1, zeros(Nregress)], [1, -an(2:end)]);
    Hz_1 = spectralfact(Hz, []);
    Hz_1_denom = Hz_1.denominator{1} / Hz_1.denominator{1}(1); % [1, -az^-1, -az^-2, ...]
    an_1 = [1, - Hz_1_denom(2:end)]; % [1, az^-1, az^-2, ...]
end