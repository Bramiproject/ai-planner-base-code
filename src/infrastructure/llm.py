import os
import pytz
from datetime import datetime
from google import genai
from google.genai import types
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from ..application.prompts import RESEARCHER_PROMPT


DREWRY_INDEX_URL = """
=== Page 1 ===

Container Freight Rate | Insight
Monthly Pricing Benchmarks on the Container Market
Contents June 2025
Summary 01-02 Transatlantic Eastbound 29-30
Transpacific Eastbound 03-06 South America Trades 31-34
Transpacific Westbound 07-09 Africa Trades 35-37
Asia-Europe 10-12 Oceania Trades 38-41
Europe-Asia 13-15 Intra-Europe Trades 42-42
Intra Asia 16-19 Drewry Weekly Rate Benchmarks 43-44
Middle East & South Asia 20-26 Appendix 45
Transatlantic Westbound 27-28
East-West spot rates set to Drewry East-West Freight Rate Index (US$/40ft)
$5,000
decline
The Drewry East-West Freight Rate Index spiked 51% to $4,000
reach $3,474 for a 40-ft box in June, after four months
of straight decline. Drewry expects spot rates on the
Transpacific and Asia-Europe trade routes to decrease. $3,000
Meanwhile, rates on the Transatlantic trade route are
expected to remain stable.
$2,000
R In e d v e e x r s s in u g rg e a d fi 3 v 6 e % -m o M n o t M h d in o w Ju n n t e re n to d , re D a r c e h w r $ y 3 ’s ,6 4 A 9 si a p - e E r u r 4 o 0 p f e t Se p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4 Ja n- 2 5 Fe b- 2 5 Mar- 2 5 A pr- 2 5 May- 2 5 J u n- 2 5
container. Spot rates were 52% lower YoY but remain
89% above the 2019 levels. Drewry expects rates to
decrease in July due to excess capacity and weakening
Drewry Global Freight Rate Index (US$/40ft)
demand.
$5,000
Drewry's Transpacific Eastbound Index surged 61% in
June to $5,791 per 40ft container, marking the second
consecutive monthly increase since President Trump
$4,000
announced the “pause” on import tariffs last month.
However, Drewry expects this trend to reverse and spot
rates to fall in July as the recent tariff-driven import
$3,000
surge is losing steam faster than expected.
Drewry's Transpacific Westbound Index decreased a
$2,000
marginal $12 to $895 per 40ft container in June. The
m
to
u lt
C
i-
h
y
i
e
n
a
a
r
h
d
a
e
s
c lin
c
e
o n
i
t
n
in u
c
e
a
d
rg o
w i
v
t
o
h
l um
ca
e
rg o
fr om
vo lu
N
m
or
e
th
in
A m
1
e
Q
ri
2
c
5
a
Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
being 9% lower than in the same period of 2024.
Drewry East-West Freight Rate Index
Our view
History
(US$/40-ft container)
Transpacific headhaul rates surged for a second
Sep-24 $4,778
consecutive month following a pause on import
tariffs. However, this upward trend is expected to Oct-24 $3,936 % change Sep 24 - Oct 24 -18%
reverse in July as the tariff-driven import surge Nov-24 $3,680 % change Oct 24 - Nov 24 -7%
loses momentum. In addition, a federal appeals
Dec-24 $3,524 % change Nov 24 - Dec 24 -4%
court has allowed President Trump's major tariffs
to remain in effect for the time being. Jan-25 $3,878 % change Dec 24 - Jan 25 10%
Feb-25 $3,002 % change Jan 25 - Feb 25 -23%
Mar-25 $2,451 % change Feb 25 - Mar 25 -18%
Apr-25 $2,334 % change Mar 25 - Apr 25 -5%
May-25 $2,302 % change Apr 25 - May 25 -1%
Jun-25 $3,474 % change May 25 - Jun 25 51%
© Drewry Supply Chain Advisors 1 June 2025


=== Page 2 ===

Global freight rates Drewry Global Freight Rate Index History*
(US$/40-ft container)
continue to slide
Sep-24 $4,265
After four consecutive months of decline, Drewry’s Global Oct-24 $3,517 % change Sep 24 - Oct 24 -18%
Freight Rate Index jumped 38% in June to reach $3,379
Nov-24 $3,505 % change Oct 24 - Nov 24 0%
per 40ft container. The surge was driven by a sharp
Dec-24 $3,431 % change Nov 24 - Dec 24 -2%
increase in rates on the Transpacific and Asia-Europe
trade routes. Jan-25 $3,786 % change Dec 24 - Jan 25 10%
Feb-25 $3,035 % change Jan 25 - Feb 25 -20%
The Intra-European Index, which tracks freight rates on
eight major European shipping routes, rose in June after Mar-25 $2,526 % change Feb 25 - Mar 25 -17%
months of stability, increasing about 17% to $1,287. Apr-25 $2,485 % change Mar 25 - Apr 25 -2%
Drewry expects rates to remain steady in July.
May-25 $2,444 % change Apr 25 - May 25 -2%
Drewry’s key South China to Brazil Index surged 128% in Jun-25 $3,379 % change May 25 - Jun 25 38%
June to $4,215 per 40ft container after declining
*Excluding Intra-Asia
consistently over the past 10 months, marking a 46% YoY
plunge. However, they remain 145% above pre-pandemic Trends in Spot Container Rates by Major
levels. The recent spike was driven by a rebound in
Trade Route/Region
cargo volumes, leading to vessel space shortages and
prompting carriers to raise rates. Short-
Recent
Major Trade Route term
Drewry's South China-South Africa Container Rate Index Trend
Forecast
jumped 30% MoM, reaching $3,278 in June, marking the
first increase in 12 months. However, the current rates Transpacific EB Rate Index (US$/40ft)
are still 62% lower year on year. This substantial rise can
Transpacific WB Rate Index (US$/40ft)
be attributed to a significant rebound in cargo volumes,
particularly as exporters hurry to send out goods in Asia-Europe WB Rate Index (US$/40ft)
anticipation of the peak season.
Asia-Europe EB Rate Index (US$/40ft)
Intra-Asia Freight Rate Index (US$/40ft)
South China-Dubai Benchmark (US$/40ft)
Transatlantic Westbound Index (US$/40ft)
Transatlantic Eastbound Index (US$/40ft)
S China-Brazil Benchmark (US$/40ft)
S China-South Africa Benchmark (US$/40ft)
S China-Australia Benchmark (US$/40ft)
Intra Europe Index (US$/40ft)
Drewry Freight Rate Indicies (US$/40ft container)
% % % %
Feb-25 Mar-25 change Apr-25 change May-25 change Jun-25 change
m-o-m m-o-m m-o-m m-o-m
Drewry global freight rate index $3,035 $2,526 -17 % $2,485 -2 % $2,444 -2 % $3,379 38 %
Drewry Regional Freight Rate Indicies (US$/40ft container)
Imports to US Rate Index $4,608 $3,538 -23 % $3,547 0 % $3,728 5 % $5,443 46 %
Imports to Europe Rate Index $3,111 $2,822 -9 % $2,642 -6 % $2,264 -14 % $3,146 39 %
Exports from US Rate Index $1,110 $1,103 -1 % $1,132 3 % $1,167 3 % $1,156 -1 %
Exports from Europe Rate Index $910 $893 -2 % $908 2 % $858 -5 % $902 5 %
Source: Drewry Maritime Research, derived from representative all-in freight rates in the major US and European
container trades
© Drewry Supply Chain Advisors 2 June 2025


=== Page 3 ===

Container Freight Rate | Insight
TRANSPACIFIC EB RATE INDEX (US$/40FT)
Tariff-driven spot rate Transpacific EB Rate Index (US$/40ft)
$7,000
surge begins to recede
$6,000
Drewry's Transpacific Eastbound Index surged 61% in June
to $5,791 per 40ft container, marking the second
consecutive monthly increase since President Trump $5,000
announced the “pause” on import tariffs last month.
However, Drewry expects this trend to reverse and spot $4,000
rates to fall in July as the recent tariff-driven import surge
is losing steam faster than expected.
$3,000
A
D
c
re
co
w
r
r
d
y
i ng
tr a
t
c
o
k s
t he
w e
W
e
o
k
r
ly
ld
s
C
p
o
o
n
t
t a
r
in
a
e
te
r
s,
I nd
fr
e
e
x
i g
(
h
W
t
C
r
I)
a
,
t e
w
s
he
f
r
r
e
o
i
m
n
Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
Shanghai to Los Angeles and New York fell sharply in the
last two weeks of June, dropping 40% to $3,741 and 23%
to $5,703 per 40ft box, respectively. Drewry Transpacific EB Rate Index (US$/40ft) Rate Index
History
In 2018, during Trump’s first term, tariffs were announced
Sep-24 $6,407
against China throughout the year, but the most significant
impact on spot rates occurred in January and August, with Oct-24 $5,707 % change Sep 24 - Oct 24 -11%
increases of 21% and 24% respectively. In contrast, the Nov-24 $5,198 % change Oct 24 - Nov 24 -9%
tariffs in 2025 have led to a much sharper increase,
Dec-24 $4,448 % change Nov 24 - Dec 24 -14%
elevating rates by over 60% in the month of June alone.
Jan-25 $5,635 % change Dec 24 - Jan 25 27%
In a latest development, a federal appeals court ruled that
Feb-25 $4,768 % change Jan 25 - Feb 25 -15%
President Trump's most sweeping tariffs can remain in
Mar-25 $3,540 % change Feb 25 - Mar 25 -26%
effect for now. The court's decision pauses a lower court's
ruling in May that had blocked the tariffs on the grounds Apr-25 $3,364 % change Mar 25 - Apr 25 -5%
that the president had exceeded his authority.
May-25 $3,603 % change Apr 25 - May 25 7%
Jun-25 $5,791 % change May 25 - Jun 25 61%
Transpacific EB Rate Index (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Yantian - New York 20ft $3,349 $3,217 $3,322 $5,348 66% 61% -19%
Yantian - New York 40ft / 40ft HC $4,413 $4,046 $4,175 $6,870 70% 65% -14%
Yantian - Los Angeles 20ft $2,457 $2,231 $2,340 $4,040 81% 73% -26%
Yantian - Los Angeles 40ft / 40ft HC $2,982 $2,782 $2,921 $5,128 84% 76% -27%
Shanghai - New York 20ft $3,151 $3,217 $3,402 $6,003 87% 76% -13%
Shanghai - New York 40ft / 40ft HC $4,112 $4,031 $4,327 $7,292 81% 69% -8%
Shanghai - Los Angeles 20ft $2,463 $2,344 $2,630 $3,727 59% 42% -31%
Shanghai - Los Angeles 40ft / 40ft HC $3,002 $2,896 $3,261 $4,993 72% 53% -25%
Hong Kong - New York 20ft $3,733 $4,280 $4,271 $7,300 71% 71% -0%
Hong Kong - New York 40ft / 40ft HC $4,626 $5,243 $5,162 $9,186 75% 78% 3%
Hong Kong - Los Angeles 20ft $2,950 $3,279 $3,354 $4,723 44% 41% -27%
Hong Kong - Los Angeles 40ft / 40ft HC $3,533 $3,683 $4,062 $5,852 59% 44% -26%
Yokohama - New York 20ft $4,409 $3,829 $3,859 $6,707 75% 74% 18%
Yokohama - New York 40ft / 40ft HC $5,357 $4,662 $4,570 $8,347 79% 83% 9%
Yokohama - Los Angeles 20ft $3,441 $2,913 $2,852 $4,662 60% 63% -7%
Yokohama - Los Angeles 40ft / 40ft HC $4,525 $3,718 $3,627 $5,941 60% 64% -8%
Busan - New York 20ft $3,088 $3,098 $3,722 $6,302 103% 69% 6%
Busan - New York 40ft / 40ft HC $3,752 $3,819 $4,565 $7,584 99% 66% 6%
Busan - Los Angeles 20ft $2,273 $2,399 $2,789 $3,335 39% 20% -36%
Busan - Los Angeles 40ft / 40ft HC $2,950 $3,000 $3,465 $4,192 40% 21% -35%
Busan - Vancouver 20ft $2,356 $2,573 $2,756 $4,084 59% 48% -20%
Busan - Vancouver 40ft / 40ft HC $2,998 $3,214 $3,398 $5,122 59% 51% -21%
Yantian - Houston 20ft $3,968 $3,862 $3,689 $6,525 69% 77% -6%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 3 June 2025


=== Page 4 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Yantian - Houston 40ft / 40ft HC $5,015 $4,648 $4,651 $8,195 76% 76% -5%
Shanghai - Houston 20ft $3,514 $3,810 $4,267 $5,049 33% 18% -34%
Shanghai - Houston 40ft / 40ft HC $4,288 $4,590 $4,936 $6,174 35% 25% -28%
Shanghai - Chicago via LA-LB 20ft $4,301 $4,125 $4,394 $5,528 34% 26% -21%
Shanghai - Chicago via LA-LB 40ft / 40ft HC $5,192 $5,142 $5,375 $6,592 28% 23% -23%
Tianjin - New York 20ft $4,395 $4,225 $4,129 $5,495 30% 33% -23%
Tianjin - New York 40ft / 40ft HC $5,160 $4,910 $4,672 $6,814 39% 46% -21%
Tianjin - Los Angeles 20ft $2,483 $2,217 $2,499 $3,856 74% 54% -37%
Tianjin - Los Angeles 40ft / 40ft HC $3,123 $2,756 $2,942 $4,675 70% 59% -39%
Tianjin - Houston 20ft $3,847 $3,717 $4,153 $7,047 90% 70% 2%
Tianjin - Houston 40ft / 40ft HC $4,804 $4,604 $4,990 $8,537 85% 71% 3%
Hong Kong - Houston 20ft $3,729 $4,081 $3,881 $6,404 57% 65% -15%
Hong Kong - Houston 40ft / 40ft HC $4,539 $4,955 $4,896 $7,970 61% 63% -12%
Yokohama - Houston 20ft $3,377 $3,485 $3,361 $5,803 67% 73% 7%
Yokohama - Houston 40ft / 40ft HC $4,297 $4,432 $4,221 $7,410 67% 76% 6%
Busan - Houston 20ft $2,967 $2,949 $3,483 $5,039 71% 45% -27%
Busan - Houston 40ft / 40ft HC $3,504 $3,531 $4,371 $6,124 73% 40% -23%
Busan - Montreal 20ft $3,810 $4,290 $4,553 $6,335 48% 39% -3%
Busan - Montreal 40ft / 40ft HC $4,631 $5,248 $5,598 $7,784 48% 39% -2%
Singapore - New York 20ft $2,907 $2,987 $2,875 $4,782 60% 66% -16%
Singapore - New York 40ft / 40ft HC $3,657 $3,767 $3,682 $6,078 61% 65% -12%
Singapore - Los Angeles 20ft $2,238 $2,422 $2,148 $2,914 20% 36% -40%
Singapore - Los Angeles 40ft / 40ft HC $2,820 $2,913 $2,736 $5,077 74% 86% -15%
Singapore - Houston 20ft $3,200 $3,280 $3,344 $4,936 50% 48% -22%
Singapore - Houston 40ft / 40ft HC $3,947 $4,042 $4,242 $6,316 56% 49% -13%
Jakarta - New York 20ft $3,069 $2,949 $3,223 $5,638 91% 75% -30%
Jakarta - New York 40ft / 40ft HC $4,008 $3,808 $4,208 $6,983 83% 66% -30%
Jakarta - Los Angeles 20ft $2,421 $2,345 $2,973 $3,771 61% 27% -39%
Jakarta - Los Angeles 40ft / 40ft HC $2,803 $2,723 $3,491 $4,657 71% 33% -43%
Yantian - Montreal 20ft $4,074 $4,493 $3,809 $5,927 32% 56% -22%
Yantian - Montreal 40ft / 40ft HC $4,894 $5,212 $4,759 $7,118 37% 50% -21%
Yantian - Halifax 20ft $3,960 $3,542 $3,437 $5,440 54% 58% -25%
Yantian - Halifax 40ft / 40ft HC $4,836 $4,343 $4,256 $6,594 52% 55% -27%
Yantian - Vancouver 20ft $2,362 $2,160 $2,250 $4,590 113% 104% -25%
Yantian - Vancouver 40ft / 40ft HC $2,940 $2,853 $3,003 $5,520 93% 84% -27%
Shanghai - Montreal 20ft $3,988 $4,314 $3,272 $6,225 44% 90% -20%
Shanghai - Montreal 40ft / 40ft HC $4,697 $4,952 $4,199 $7,508 52% 79% -17%
Shanghai - Halifax 20ft $4,323 $3,480 $3,286 $5,433 56% 65% -26%
Shanghai - Halifax 40ft / 40ft HC $5,344 $4,306 $4,072 $6,749 57% 66% -21%
Shanghai - Vancouver 20ft $2,434 $1,977 $2,225 $4,846 145% 118% -22%
Shanghai - Vancouver 40ft / 40ft HC $2,919 $2,710 $3,060 $6,089 125% 99% -19%
Tianjin - Montreal 20ft $4,908 $4,936 $4,960 $7,668 55% 55% 7%
Tianjin - Montreal 40ft / 40ft HC $5,884 $5,875 $5,898 $9,198 57% 56% 8%
Tianjin - Vancouver 20ft $3,270 $2,803 $2,693 $5,180 85% 92% -12%
Tianjin - Vancouver 40ft / 40ft HC $3,921 $3,671 $3,544 $6,420 75% 81% -11%
Hong Kong - Montreal 20ft $4,307 $4,479 $3,973 $6,640 48% 67% -19%
Hong Kong - Montreal 40ft / 40ft HC $5,150 $5,479 $4,958 $8,109 48% 64% -15%
Hong Kong - Halifax 20ft $3,343 $4,006 $3,486 $6,300 57% 81% -21%
Hong Kong - Halifax 40ft / 40ft HC $4,082 $5,038 $4,321 $7,819 55% 81% -18%
Hong Kong - Vancouver 20ft $2,543 $2,786 $2,539 $5,349 92% 111% -20%
Hong Kong - Vancouver 40ft / 40ft HC $3,139 $3,471 $3,204 $6,471 86% 102% -22%
Singapore - Montreal 20ft $3,777 $3,684 $3,552 $3,816 4% 7% -55%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 4 June 2025


=== Page 5 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Singapore - Montreal 40ft / 40ft HC $4,734 $4,415 $4,281 $5,005 13% 17% -52%
Singapore - Halifax 20ft $3,706 $3,653 $3,522 $4,825 32% 37% -39%
Singapore - Halifax 40ft / 40ft HC $4,558 $4,558 $4,345 $6,024 32% 39% -39%
Singapore - Vancouver 20ft $2,557 $2,554 $2,347 $4,474 75% 91% -40%
Singapore - Vancouver 40ft / 40ft HC $3,217 $3,128 $2,880 $5,741 84% 99% -39%
Manila - New York 20ft $3,358 $3,751 $3,849 $4,541 21% 18% -32%
Manila - New York 40ft / 40ft HC $4,042 $4,479 $4,740 $5,214 16% 10% -34%
Manila - Los Angeles 20ft $2,448 $2,892 $3,028 $3,655 26% 21% -32%
Manila - Los Angeles 40ft / 40ft HC $3,056 $3,503 $3,741 $4,575 31% 22% -32%
Manila - Houston 20ft $3,741 $4,050 $3,867 $4,541 12% 17% -41%
Manila - Houston 40ft / 40ft HC $4,405 $4,744 $4,792 $5,653 19% 18% -37%
Ho Chi Minh City - New York 20ft $3,388 $3,346 $3,850 $4,810 44% 25% -29%
Ho Chi Minh City - New York 40ft / 40ft HC $4,145 $4,036 $4,608 $5,778 43% 25% -28%
Ho Chi Minh City - Los Angeles 20ft $2,548 $2,527 $2,827 $3,447 36% 22% -40%
Ho Chi Minh City - Los Angeles 40ft / 40ft HC $3,166 $3,096 $3,507 $4,286 38% 22% -39%
Ho Chi Minh City - Houston 20ft $3,260 $3,341 $3,746 $4,855 45% 30% -26%
Ho Chi Minh City - Houston 40ft / 40ft HC $4,067 $4,095 $4,586 $5,780 41% 26% -26%
Laem Chabang - New York 20ft $3,388 $3,533 $3,795 $6,233 76% 64% -30%
Laem Chabang - New York 40ft / 40ft HC $4,080 $4,417 $4,740 $7,928 79% 67% -12%
Laem Chabang - Los Angeles 20ft $2,440 $2,065 $3,033 $4,557 121% 50% -31%
Laem Chabang - Los Angeles 40ft / 40ft HC $3,071 $2,738 $3,501 $5,250 92% 50% -34%
Laem Chabang - Houston 20ft $3,067 $2,902 $3,696 $5,485 89% 48% -25%
Laem Chabang - Houston 40ft / 40ft HC $3,651 $3,598 $4,407 $6,837 90% 55% -20%
Tanjung Pelepas - New York 20ft $2,818 $3,169 $3,084 $5,557 75% 80% -22%
Tanjung Pelepas - New York 40ft / 40ft HC $3,430 $3,848 $3,803 $6,975 81% 83% -17%
Tanjung Pelepas - Los Angeles 20ft $1,972 $2,323 $2,261 $3,610 55% 60% -42%
Tanjung Pelepas - Los Angeles 40ft / 40ft HC $2,418 $2,796 $2,766 $4,530 62% 64% -40%
Tanjung Pelepas - Houston 20ft $2,935 $3,254 $3,538 $5,455 68% 54% -31%
Tanjung Pelepas - Houston 40ft / 40ft HC $3,535 $3,917 $4,404 $6,758 73% 53% -27%
Kaohsiung - New York 20ft $3,373 $3,198 $3,302 $5,758 80% 74% -16%
Kaohsiung - New York 40ft / 40ft HC $4,030 $3,840 $4,285 $6,863 79% 60% -18%
Kaohsiung - Los Angeles 20ft $2,255 $2,165 $2,486 $4,608 113% 85% -10%
Kaohsiung - Los Angeles 40ft / 40ft HC $2,774 $2,700 $3,118 $5,796 115% 86% -12%
Kaohsiung - Houston 20ft $3,845 $3,366 $3,434 $6,234 85% 82% -17%
Kaohsiung - Houston 40ft / 40ft HC $4,450 $4,397 $4,501 $7,829 78% 74% -8%
Shanghai - Memphis via Los Angeles 20ft $5,240 $4,620 $4,620 $6,342 37% 37% -22%
Shanghai - Memphis via Los Angeles 40ft / 40ft HC $5,991 $5,341 $6,107 $7,576 42% 24% -16%
Shanghai - Toronto via New York 20ft $4,728 $4,060 $3,765 $6,014 48% 60% -15%
Shanghai - Toronto via New York 40ft / 40ft HC $5,644 $4,894 $4,433 $7,214 47% 63% -11%
Shanghai - Toronto via Vancouver 20ft $4,100 $4,138 $3,973 $7,190 74% 81% 8%
Shanghai - Toronto via Vancouver 40ft / 40ft HC $5,012 $5,074 $5,548 $8,373 65% 51% 4%
Colombo - New York 20ft $3,064 $2,740 $3,107 $5,013 83% 61% 57%
Colombo - New York 40ft / 40ft HC $3,573 $3,206 $3,622 $5,606 75% 55% 26%
Chittagong - New York 20ft $4,106 $3,755 $4,186 $5,373 43% 28% 29%
Chittagong - New York 40ft / 40ft HC $4,951 $4,368 $5,026 $6,123 40% 22% 23%
Shanghai - Kansas City via Los Angeles 20ft $4,639 $4,539 $4,252 $6,788 50% 60% -8%
Shanghai - Kansas City via Los Angeles 40ft / 40ft HC $5,645 $5,805 $5,739 $8,448 46% 47% -6%
Laem Chabang - Chicago via Los Angeles 20ft $4,348 $4,064 $4,438 $6,714 65% 51% -3%
Laem Chabang - Chicago via Los Angeles 40ft / 40ft HC $5,444 $5,018 $5,368 $8,058 61% 50% -5%
Yokohama - Chicago via Prince Rupert 20ft $4,514 $4,905 $4,822 $6,765 38% 40% 26%
Yokohama - Chicago via Prince Rupert 40ft / 40ft HC $5,739 $5,977 $5,877 $8,331 39% 42% 12%
Yokohama - Manzanillo (Mexico) 20ft $3,150 $2,315 $2,362 $3,446 49% 46% -39%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 5 June 2025


=== Page 6 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Yokohama - Manzanillo (Mexico) 40ft / 40ft HC $4,019 $2,928 $3,262 $4,474 53% 37% -36%
Yantian - Chicago via Los Angeles 20ft $4,609 $4,130 $3,706 $5,946 44% 60% -9%
Yantian - Chicago via Los Angeles 40ft / 40ft HC $5,627 $5,130 $4,397 $7,308 42% 66% -8%
Busan - Chicago via Los Angeles 20ft $3,764 $3,998 $3,727 $5,463 37% 47% -9%
Busan - Chicago via Los Angeles 40ft / 40ft HC $4,752 $4,872 $4,566 $6,760 39% 48% -3%
Yokohama - Chicago via Los Angeles 20ft $5,036 $4,833 $4,743 $6,626 37% 40% 20%
Yokohama - Chicago via Los Angeles 40ft / 40ft HC $6,378 $5,888 $5,764 $7,987 36% 39% 17%
Shanghai - Memphis via Savannah 20ft $5,279 $4,316 $4,523 $7,645 77% 69% 11%
Shanghai - Memphis via Savannah 40ft / 40ft HC $6,435 $5,301 $5,350 $8,544 61% 60% 5%
Shanghai - Jacksonville 20ft $5,088 $4,523 $4,456 $6,102 35% 37% -6%
Shanghai - Jacksonville 40ft / 40ft HC $6,467 $5,256 $5,140 $7,402 41% 44% -3%
Ho Chi Minh City - Montreal 20ft $4,353 $4,751 $4,340 $7,129 50% 64% 4%
Ho Chi Minh City - Montreal 40ft / 40ft HC $5,186 $5,659 $5,310 $8,593 52% 62% 6%
Ho Chi Minh City - Vancouver 20ft $2,384 $2,724 $2,500 $5,251 93% 110% -3%
Ho Chi Minh City - Vancouver 40ft / 40ft HC $3,008 $3,457 $3,189 $6,572 90% 106% -4%
Shanghai - Manzanillo (Mexico) 20ft $2,023 $1,719 $1,726 $3,845 124% 123% -42%
Shanghai - Manzanillo (Mexico) 40ft / 40ft HC $2,352 $2,074 $2,230 $4,346 110% 95% -45%
Los Angeles - Manzanillo (Mexico) 20ft $1,702 $2,055 $2,164 $2,419 18% 12% 24%
Los Angeles - Manzanillo (Mexico) 40ft / 40ft HC $2,443 $2,911 $3,060 $3,436 18% 12% 36%
Ho Chi Minh City - Manzanillo (Mexico) 20ft $1,648 $1,734 $1,701 $2,452 41% 44% -59%
Ho Chi Minh City - Manzanillo (Mexico) 40ft / 40ft HC $2,236 $2,286 $2,288 $3,105 36% 36% -56%
Yokohama - Prince Rupert 20ft $3,935 $2,943 $2,791 $5,198 77% 86% -3%
Yokohama - Prince Rupert 40ft / 40ft HC $5,597 $3,680 $3,404 $6,500 77% 91% -13%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 6 June 2025


=== Page 7 ===

Container Freight Rate | Insight
TRANSPACIFIC WB RATE INDEX (US$/40FT)
US container exports Transpacific WB Rate Index (US$/40ft)
$1,000
to China plummet
Drewry's Transpacific Westbound Index decreased a
$950
marginal $12 to $895 per 40ft container in June. Although
freight rates have been largely stable over the past year,
spot rates are below 2019 levels. Drewry anticipates that
$900
this low-rate environment will persist, expecting rates to
hold steady next month.
$850
According to the latest demand data, the multi-year
d
co
e
n
c
t
li
i
n
n
e
u e
in
d w
ca
it
r
h
g o
c a
v
r
o
g
l
o
u m
vo
e
l u
f
m
ro
e
m
i n
N o
1
r
Q
th
2 5
A
b
m
e
e
in
ri
g
c a
9 %
to
lo
C
w
hi
e
n
r
a
t h
h
a
a
n
s
Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
in the same period of 2024. Compared to previous years,
1Q25 volumes were also down 18% YoY from 2019, 13%
YoY from 2020 and 14% YoY from 2021. Drewry Transpacific WB Rate Index (US$/40ft) Rate Index
History
US exporters of agricultural products like grains, cotton and
Sep-24 $975
fruits are expected to encounter their most significant
obstacles by far when shipping to China. This is because Oct-24 $970 % change Sep 24 - Oct 24 0%
China, still the primary market for US farm exports, is Nov-24 $918 % change Oct 24 - Nov 24 -5%
actively retaliating with various measures due to the
Dec-24 $922 % change Nov 24 - Dec 24 0%
substantial tariffs imposed by the Trump administration on
Chinese imports. Jan-25 $934 % change Dec 24 - Jan 25 1%
Feb-25 $888 % change Jan 25 - Feb 25 -5%
Initially, China announced tariffs of up to 125% aiming to
Mar-25 $871 % change Feb 25 - Mar 25 -2%
hit US agricultural and forest product exports,but
thereafter reduced these import duties significantly to 10% Apr-25 $896 % change Mar 25 - Apr 25 3%
amid the 90-day tariff reprieve that expires in mid-August.
May-25 $907 % change Apr 25 - May 25 1%
Jun-25 $895 % change May 25 - Jun 25 -1%
Transpacific WB Rate Index (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
New York - Yantian 20ft $678 $684 $805 $776 13% -4% -8%
New York - Yantian 40ft / 40ft HC $795 $813 $935 $866 7% -7% -20%
Los Angeles - Yantian 20ft $608 $547 $467 $478 -13% 2% -20%
Los Angeles - Yantian 40ft / 40ft HC $684 $633 $556 $574 -9% 3% -25%
New York - Shanghai 20ft $927 $956 $954 $954 -0% 0% 18%
New York - Shanghai 40ft / 40ft HC $1,114 $1,142 $1,124 $1,138 -0% 1% 14%
Los Angeles - Shanghai 20ft $580 $574 $573 $591 3% 3% 28%
Los Angeles - Shanghai 40ft / 40ft HC $785 $789 $788 $773 -2% -2% 15%
New York - Hong Kong 20ft $981 $1,119 $1,159 $1,161 4% 0% 16%
New York - Hong Kong 40ft / 40ft HC $1,213 $1,397 $1,458 $1,409 1% -3% 14%
Los Angeles - Hong Kong 20ft $934 $946 $998 $1,035 9% 4% -14%
Los Angeles - Hong Kong 40ft / 40ft HC $1,132 $1,108 $1,294 $1,260 14% -3% -3%
New York - Yokohama 20ft $1,267 $1,544 $1,502 $1,472 -5% -2% 3%
New York - Yokohama 40ft / 40ft HC $1,568 $1,924 $1,770 $1,716 -11% -3% -7%
Los Angeles - Yokohama 20ft $913 $892 $876 $810 -9% -8% -15%
Los Angeles - Yokohama 40ft / 40ft HC $945 $925 $1,050 $1,007 9% -4% -15%
New York - Busan 20ft $698 $832 $871 $867 4% -0% 10%
New York - Busan 40ft / 40ft HC $859 $1,055 $1,110 $1,068 1% -4% 16%
Los Angeles - Busan 20ft $621 $816 $784 $784 -4% 0% 19%
Los Angeles - Busan 40ft / 40ft HC $812 $940 $936 $964 3% 3% 16%
Toronto via New York - Shanghai 20ft $1,788 $1,581 $1,581 $1,550 -2% -2% -34%
Toronto via New York - Shanghai 40ft / 40ft HC $2,152 $1,827 $1,827 $1,870 2% 2% -41%
Toronto via Vancouver - Shanghai 20ft $1,396 $1,229 $1,330 $1,386 13% 4% 9%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 7 June 2025


=== Page 8 ===

Container Freight Rate | Insight
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Toronto via Vancouver - Shanghai 40ft / 40ft HC $1,601 $1,433 $1,619 $1,779 24% 10% 10%
Halifax - Shanghai 20ft $1,420 $1,409 $1,246 $1,270 -10% 2% -4%
Halifax - Shanghai 40ft / 40ft HC $1,855 $1,845 $1,597 $1,560 -15% -2% -6%
Halifax - Hong Kong 20ft $1,605 $1,604 $1,400 $1,394 -13% -0% -9%
Halifax - Hong Kong 40ft / 40ft HC $2,082 $2,081 $1,766 $1,714 -18% -3% -12%
Halifax - Singapore 20ft $1,242 $1,242 $1,113 $1,248 0% 12% -16%
Halifax - Singapore 40ft / 40ft HC $1,514 $1,514 $1,307 $1,454 -4% 11% -16%
Halifax - Yantian 20ft $1,615 $1,615 $1,441 $1,437 -11% -0% -14%
Halifax - Yantian 40ft / 40ft HC $2,053 $2,052 $1,789 $1,722 -16% -4% -17%
Montreal - Shanghai 20ft $1,426 $1,459 $1,289 $1,504 3% 17% 0%
Montreal - Shanghai 40ft / 40ft HC $1,758 $1,833 $1,645 $1,852 1% 13% 4%
Montreal - Hong Kong 20ft $1,673 $1,786 $1,558 $1,530 -14% -2% -13%
Montreal - Hong Kong 40ft / 40ft HC $2,018 $2,191 $1,958 $1,908 -13% -3% -6%
Montreal - Busan 20ft $1,257 $1,151 $1,151 $1,111 -3% -3% -20%
Montreal - Busan 40ft / 40ft HC $1,562 $1,486 $1,519 $1,459 -2% -4% -12%
Montreal - Tianjin 20ft $931 $1,505 $1,122 $1,246 -17% 11% -20%
Montreal - Tianjin 40ft / 40ft HC $1,197 $1,930 $1,415 $1,545 -20% 9% -17%
Montreal - Singapore 20ft $1,345 $1,468 $1,388 $1,363 -7% -2% -9%
Montreal - Singapore 40ft / 40ft HC $1,575 $1,782 $1,780 $1,873 5% 5% 7%
Montreal - Yantian 20ft $1,217 $1,476 $1,304 $1,316 -11% 1% -20%
Montreal - Yantian 40ft / 40ft HC $1,481 $1,846 $1,662 $1,683 -9% 1% -9%
Vancouver - Shanghai 20ft $1,133 $922 $713 $643 -30% -10% -35%
Vancouver - Shanghai 40ft / 40ft HC $1,375 $1,133 $831 $795 -30% -4% -39%
Vancouver - Hong Kong 20ft $1,262 $1,204 $1,015 $1,373 14% 35% 3%
Vancouver - Hong Kong 40ft / 40ft HC $1,523 $1,488 $1,191 $1,541 4% 29% -1%
Vancouver - Busan 20ft $1,226 $1,158 $1,220 $1,142 -1% -6% -8%
Vancouver - Busan 40ft / 40ft HC $1,172 $1,122 $1,325 $1,272 13% -4% -1%
Vancouver - Tianjin 20ft $1,010 $845 $757 $1,307 55% 73% 20%
Vancouver - Tianjin 40ft / 40ft HC $1,294 $1,127 $999 $1,253 11% 25% 13%
Vancouver - Singapore 20ft $1,159 $1,183 $992 $1,286 9% 30% -3%
Vancouver - Singapore 40ft / 40ft HC $1,250 $1,479 $1,072 $1,389 -6% 30% 1%
Vancouver - Yantian 20ft $1,231 $1,122 $941 $1,245 11% 32% 20%
Vancouver - Yantian 40ft / 40ft HC $1,418 $1,265 $989 $1,338 6% 35% 17%
Manzanillo (Mexico) - Yokohama 20ft $692 $601 $561 $674 12% 20% -43%
Manzanillo (Mexico) - Yokohama 40ft / 40ft HC $998 $849 $787 $820 -3% 4% -51%
New York - Tanjung Pelepas 20ft $1,201 $1,339 $1,481 $1,300 -3% -12% 16%
New York - Tanjung Pelepas 40ft / 40ft HC $1,472 $1,652 $1,837 $1,525 -8% -17% 14%
New York - Tianjin 20ft $1,373 $1,346 $1,310 $1,077 -20% -18% -31%
New York - Tianjin 40ft / 40ft HC $1,634 $1,610 $1,208 $1,181 -27% -2% -36%
New York - Manila 20ft $1,697 $1,834 $1,451 $1,477 -19% 2% -7%
New York - Manila 40ft / 40ft HC $2,361 $2,550 $1,920 $1,910 -25% -1% -12%
New York - Singapore 20ft $625 $696 $807 $895 29% 11% 81%
New York - Singapore 40ft / 40ft HC $726 $844 $892 $942 12% 6% 43%
New York - Kaohsiung 20ft $900 $1,037 $1,041 $1,187 14% 14% 26%
New York - Kaohsiung 40ft / 40ft HC $1,082 $1,264 $1,312 $1,449 15% 10% 28%
New York - Laem Chabang 20ft $882 $857 $841 $1,052 23% 25% -6%
New York - Laem Chabang 40ft / 40ft HC $1,141 $1,210 $1,161 $1,297 7% 12% -3%
New York - Ho Chi Minh City 20ft $865 $1,002 $1,065 $1,072 7% 1% 101%
New York - Ho Chi Minh City 40ft / 40ft HC $1,095 $1,278 $1,357 $1,328 4% -2% 95%
Houston - Shanghai 20ft $855 $848 $839 $848 0% 1% 2%
Houston - Shanghai 40ft / 40ft HC $1,021 $1,010 $975 $995 -1% 2% -8%
Houston - Hong Kong 20ft $1,188 $1,292 $1,123 $1,230 -5% 10% -11%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 8 June 2025


=== Page 9 ===

Container Freight Rate | Insight
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Houston - Hong Kong 40ft / 40ft HC $1,562 $1,699 $1,488 $1,588 -7% 7% -8%
Houston - Yokohama 20ft $1,674 $1,607 $1,582 $1,611 0% 2% 25%
Houston - Yokohama 40ft / 40ft HC $1,896 $1,795 $1,722 $1,786 -1% 4% 10%
Houston - Busan 20ft $1,084 $1,188 $1,052 $1,056 -11% 0% -23%
Houston - Busan 40ft / 40ft HC $1,276 $1,428 $1,340 $1,309 -8% -2% -21%
Houston - Tanjung Pelepas 20ft $1,373 $1,511 $1,693 $1,813 20% 7% 15%
Houston - Tanjung Pelepas 40ft / 40ft HC $1,880 $2,060 $2,401 $2,461 19% 2% 20%
Houston - Tianjin 20ft $1,268 $1,266 $1,189 $1,376 9% 16% -17%
Houston - Tianjin 40ft / 40ft HC $1,623 $1,631 $1,488 $1,417 -13% -5% -31%
Houston - Manila 20ft $1,531 $1,670 $1,530 $1,555 -7% 2% 16%
Houston - Manila 40ft / 40ft HC $1,974 $2,164 $1,982 $1,972 -9% -1% 17%
Houston - Singapore 20ft $982 $1,068 $1,164 $1,244 16% 7% 34%
Houston - Singapore 40ft / 40ft HC $1,162 $1,158 $1,449 $1,653 43% 14% 48%
Houston - Yantian 20ft $1,142 $1,221 $1,055 $1,046 -14% -1% -25%
Houston - Yantian 40ft / 40ft HC $1,278 $1,502 $1,319 $1,264 -16% -4% -16%
Houston - Kaohsiung 20ft $1,175 $1,312 $1,194 $1,340 2% 12% 15%
Houston - Kaohsiung 40ft / 40ft HC $1,624 $1,809 $1,687 $1,824 1% 8% 12%
Houston - Laem Chabang 20ft $1,343 $1,506 $1,331 $1,336 -11% 0% -13%
Houston - Laem Chabang 40ft / 40ft HC $1,828 $2,168 $1,804 $1,773 -18% -2% -10%
Houston - Ho Chi Minh City 20ft $1,174 $1,290 $1,252 $1,278 -1% 2% -7%
Houston - Ho Chi Minh City 40ft / 40ft HC $1,464 $1,601 $1,557 $1,585 -1% 2% -4%
Chicago via LA-LB - Shanghai 20ft $920 $911 $1,210 $1,280 41% 6% 10%
Chicago via LA-LB - Shanghai 40ft / 40ft HC $1,173 $1,164 $1,430 $1,713 47% 20% 34%
Memphis via Los Angeles - Shanghai 20ft $1,524 $1,541 $1,441 $1,501 -3% 4% 41%
Memphis via Los Angeles - Shanghai 40ft / 40ft HC $1,880 $1,921 $1,921 $1,855 -3% -3% 52%
Memphis via Savannah - Shanghai 20ft $1,273 $1,183 $1,183 $1,104 -7% -7% -28%
Memphis via Savannah - Shanghai 40ft / 40ft HC $1,531 $1,362 $1,362 $1,241 -9% -9% -28%
Los Angeles - Tanjung Pelepas 20ft $1,196 $1,451 $1,393 $1,495 3% 7% 12%
Los Angeles - Tanjung Pelepas 40ft / 40ft HC $1,515 $1,988 $1,909 $1,876 -6% -2% 27%
Los Angeles - Tianjin 20ft $832 $790 $815 $917 16% 13% -21%
Los Angeles - Tianjin 40ft / 40ft HC $994 $988 $1,052 $1,220 23% 16% -11%
Los Angeles - Manila 20ft $1,541 $2,104 $1,248 $1,273 -39% 2% -25%
Los Angeles - Manila 40ft / 40ft HC $2,154 $2,793 $1,568 $1,559 -44% -1% -23%
Los Angeles - Singapore 20ft $995 $914 $916 $815 -11% -11% 17%
Los Angeles - Singapore 40ft / 40ft HC $1,279 $1,181 $1,158 $961 -19% -17% 9%
Los Angeles - Kaohsiung 20ft $739 $877 $906 $1,052 20% 16% 33%
Los Angeles - Kaohsiung 40ft / 40ft HC $936 $1,119 $1,161 $1,297 16% 12% 33%
Los Angeles - Laem Chabang 20ft $737 $833 $829 $924 11% 11% -18%
Los Angeles - Laem Chabang 40ft / 40ft HC $882 $1,123 $1,082 $1,151 2% 6% -11%
Los Angeles - Ho Chi Minh City 20ft $795 $911 $920 $920 1% 0% 14%
Los Angeles - Ho Chi Minh City 40ft / 40ft HC $984 $1,151 $1,208 $1,169 2% -3% 10%
Montreal - Ho Chi Minh City 20ft $1,720 $1,666 $1,618 $1,575 -5% -3% -7%
Montreal - Ho Chi Minh City 40ft / 40ft HC $2,448 $2,153 $2,135 $2,197 2% 3% 3%
Vancouver - Ho Chi Minh City 20ft $1,595 $1,269 $1,274 $1,627 28% 28% 23%
Vancouver - Ho Chi Minh City 40ft / 40ft HC $1,650 $1,539 $1,316 $1,609 5% 22% 11%
Manzanillo (Mexico) - Shanghai 20ft $706 $819 $819 $777 -5% -5% 6%
Manzanillo (Mexico) - Shanghai 40ft / 40ft HC $939 $1,050 $1,050 $1,017 -3% -3% -5%
Manzanillo (Mexico) - Los Angeles 20ft $1,383 $1,251 $1,446 $1,509 21% 4% 13%
Manzanillo (Mexico) - Los Angeles 40ft / 40ft HC $1,605 $1,634 $1,747 $1,839 13% 5% 5%
Prince Rupert - Yokohama 20ft $2,092 $1,635 $1,485 $1,421 -13% -4% -36%
Prince Rupert - Yokohama 40ft / 40ft HC $2,551 $2,019 $1,825 $1,786 -12% -2% -29%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 9 June 2025


=== Page 10 ===

Container Freight Rate | Insight
ASIA-EUROPE WB RATE INDEX (US$/40FT)
June FAKs reverse 5- Asia-Europe WB Rate Index (US$/40ft)
$6,000
month rate slide
$5,000
Reversing a five-month downtrend, Drewry’s Asia-Europe
Index surged 36% MoM in June to reach $3,649 per 40ft
$4,000
container. Spot rates were 52% lower YoY but remain 89%
above the 2019 levels. Drewry expects rates to decrease in
July due to excess capacity and weakening demand. $3,000
In May, several carriers announced ambitious FAKs of over
$3,000 per 40ft container to halt the spot market's slide. $2,000
W
th
h
e
i l
fi
e
r s
t
t
h
w
e
e
s
e
t
k
ra
o
te
f
g
Ju
y
n
w
e,
a
t
s
h e
in
g
it
a
ia
in
ll
s
y
w
su
e
c
re
c e
s
s
h
s
o
fu
rt
l
-
,
l i
l
v
if
e
t
d
in
,
g
a n
ra
d
t
r
e
a
s
t e
in
s Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
stabilised shortly thereafter.
According to the World Container Index (WCI), wherein
Drewry tracks weekly spot rates, freight rates from Drewry Asia-Europe WB Rate Index (US$/40ft) Rate Index
History
Shanghai to Rotterdam and Genoa increased sharply in the
first week of June, gaining 32% to $2,845 and 38% to
Sep-24 $5,682
$4,068 per 40ft box, respectively. However, spot rates
Oct-24 $4,003 % change Sep 24 - Oct 24 -30%
remained stable for the rest of the month.
Nov-24 $4,729 % change Oct 24 - Nov 24 18%
The Gemini Cooperation's new "hub-and-spoke" strategy
Dec-24 $5,595 % change Nov 24 - Dec 24 18%
concentrates massive cargo volumes into select hub ports
like London Gateway. While this model is designed to boost Jan-25 $4,634 % change Dec 24 - Jan 25 -17%
schedule reliability, it creates a high risk of severe Feb-25 $3,660 % change Jan 25 - Feb 25 -21%
congestion. If a hub port cannot manage these
Mar-25 $3,266 % change Feb 25 - Mar 25 -11%
concentrated surges, it results in critical bottlenecks,
including vessel delays and backlogs for inland truck and Apr-25 $2,961 % change Mar 25 - Apr 25 -9%
rail transport.
May-25 $2,675 % change Apr 25 - May 25 -10%
Jun-25 $3,649 % change May 25 - Jun 25 36%
Asia-Europe WB Rate Index (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Shanghai - Rotterdam 20ft $1,769 $1,705 $1,608 $2,200 29% 37% -51%
Shanghai - Rotterdam 40ft / 40ft HC $2,959 $2,755 $2,462 $3,380 23% 37% -54%
Shanghai - Genoa 20ft $2,728 $2,584 $2,364 $3,410 32% 44% -43%
Shanghai - Genoa 40ft / 40ft HC $3,788 $3,364 $3,217 $4,452 32% 38% -40%
Yokohama - Rotterdam 20ft $2,758 $2,123 $1,835 $2,153 1% 17% -61%
Yokohama - Rotterdam 40ft / 40ft HC $4,350 $3,490 $2,987 $3,598 3% 20% -63%
Yokohama - Genoa 20ft $3,189 $2,770 $2,595 $2,762 -0% 6% -49%
Yokohama - Genoa 40ft / 40ft HC $5,030 $4,444 $4,106 $4,354 -2% 6% -50%
Busan - Rotterdam 20ft $1,786 $1,695 $1,511 $2,271 34% 50% -54%
Busan - Rotterdam 40ft / 40ft HC $2,857 $2,665 $2,289 $3,485 31% 52% -57%
Busan - Genoa 20ft $2,600 $2,464 $2,413 $3,494 42% 45% -37%
Busan - Genoa 40ft / 40ft HC $3,640 $3,278 $3,215 $4,930 50% 53% -35%
Chittagong - Rotterdam 20ft $2,362 $2,366 $1,893 $1,983 -16% 5% -34%
Chittagong - Rotterdam 40ft / 40ft HC $2,833 $2,752 $2,196 $2,347 -15% 7% -44%
Shanghai - Helsinki 20ft $2,029 $1,758 $1,607 $2,220 26% 38% -49%
Shanghai - Helsinki 40ft / 40ft HC $2,988 $2,834 $2,559 $3,479 23% 36% -52%
Shanghai - Gdansk 20ft $1,546 $1,353 $1,299 $2,059 52% 59% -49%
Shanghai - Gdansk 40ft / 40ft HC $2,368 $2,094 $2,011 $3,254 55% 62% -53%
Shanghai - Saint Petersburg 20ft $4,030 $3,830 $4,296 $4,363 14% 2% -33%
Shanghai - Saint Petersburg 40ft / 40ft HC $5,164 $5,081 $5,997 $5,631 11% -6% -32%
Shanghai - Gothenburg 20ft $1,454 $1,340 $1,517 $2,089 56% 38% -45%
Shanghai - Gothenburg 40ft / 40ft HC $2,211 $1,958 $2,203 $3,237 65% 47% -52%
Shanghai - Istanbul 20ft $2,690 $2,384 $2,387 $3,147 32% 32% -43%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 10 June 2025


=== Page 11 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Shanghai - Istanbul 40ft / 40ft HC $3,458 $3,136 $3,121 $4,281 37% 37% -44%
Shanghai - Felixstowe 20ft $1,860 $1,831 $1,548 $2,151 17% 39% -54%
Shanghai - Felixstowe 40ft / 40ft HC $2,936 $2,851 $2,242 $3,300 16% 47% -59%
Hong Kong - Rotterdam 20ft $2,514 $1,746 $1,798 $2,743 57% 53% -41%
Hong Kong - Rotterdam 40ft / 40ft HC $4,006 $2,689 $2,744 $4,167 55% 52% -41%
Hong Kong - Felixstowe 20ft $2,043 $1,960 $1,500 $2,478 26% 65% -52%
Hong Kong - Felixstowe 40ft / 40ft HC $3,118 $2,935 $2,342 $3,816 30% 63% -56%
Hong Kong - Genoa 20ft $2,945 $2,945 $2,769 $3,284 12% 19% -43%
Hong Kong - Genoa 40ft / 40ft HC $3,984 $4,134 $3,807 $4,742 15% 25% -42%
Jakarta - Rotterdam 20ft $2,467 $1,957 $1,766 $2,217 13% 26% -56%
Jakarta - Rotterdam 40ft / 40ft HC $3,921 $3,012 $2,711 $3,410 13% 26% -56%
Jakarta - Felixstowe 20ft $1,976 $1,843 $1,743 $2,274 23% 30% -64%
Jakarta - Felixstowe 40ft / 40ft HC $2,811 $2,598 $2,528 $3,269 26% 29% -67%
Jakarta - Genoa 20ft $2,650 $2,650 $2,622 $2,949 11% 12% -53%
Jakarta - Genoa 40ft / 40ft HC $3,809 $3,809 $3,819 $4,259 12% 12% -53%
Yokohama - Felixstowe 20ft $2,572 $2,249 $1,934 $2,459 9% 27% -50%
Yokohama - Felixstowe 40ft / 40ft HC $4,256 $3,472 $3,286 $4,075 17% 24% -53%
Busan - Felixstowe 20ft $1,958 $1,868 $1,416 $2,483 33% 75% -39%
Busan - Felixstowe 40ft / 40ft HC $3,040 $2,948 $2,321 $3,707 26% 60% -48%
Tanjung Pelepas - Rotterdam 20ft $2,259 $1,571 $1,332 $2,426 54% 82% -45%
Tanjung Pelepas - Rotterdam 40ft / 40ft HC $3,719 $2,516 $2,260 $3,672 46% 62% -46%
Tanjung Pelepas - Felixstowe 20ft $1,809 $1,693 $1,449 $2,357 39% 63% -50%
Tanjung Pelepas - Felixstowe 40ft / 40ft HC $2,832 $2,622 $2,403 $3,608 38% 50% -56%
Tanjung Pelepas - Genoa 20ft $2,955 $2,902 $2,679 $3,632 25% 36% -33%
Tanjung Pelepas - Genoa 40ft / 40ft HC $3,990 $3,895 $3,579 $5,010 29% 40% -47%
Tianjin - Port Said 20ft $3,181 $2,515 $2,446 $3,525 40% 44% -34%
Tianjin - Port Said 40ft / 40ft HC $4,316 $3,833 $3,261 $5,193 35% 59% -31%
Tianjin - Rotterdam 20ft $1,674 $1,440 $1,597 $2,528 76% 58% -41%
Tianjin - Rotterdam 40ft / 40ft HC $2,606 $2,101 $2,142 $3,916 86% 83% -47%
Tianjin - Saint Petersburg 20ft $4,239 $4,373 $3,806 $4,906 12% 29% -21%
Tianjin - Saint Petersburg 40ft / 40ft HC $5,777 $6,144 $5,244 $6,477 5% 24% -25%
Tianjin - Istanbul 20ft $3,160 $2,687 $2,448 $3,914 46% 60% -28%
Tianjin - Istanbul 40ft / 40ft HC $4,377 $3,447 $3,411 $5,190 51% 52% -31%
Tianjin - Felixstowe 20ft $1,839 $1,456 $1,276 $2,065 42% 62% -56%
Tianjin - Felixstowe 40ft / 40ft HC $3,085 $2,332 $1,815 $3,286 41% 81% -61%
Tianjin - Genoa 20ft $3,089 $3,240 $2,617 $3,834 18% 47% -29%
Tianjin - Genoa 40ft / 40ft HC $4,318 $4,512 $3,414 $5,417 20% 59% -26%
Yantian - Port Said 20ft $3,079 $2,277 $2,014 $3,590 58% 78% -32%
Yantian - Port Said 40ft / 40ft HC $4,324 $3,512 $3,169 $5,098 45% 61% -32%
Yantian - Rotterdam 20ft $1,643 $1,424 $1,353 $2,059 45% 52% -57%
Yantian - Rotterdam 40ft / 40ft HC $2,456 $2,193 $2,065 $3,278 49% 59% -59%
Yantian - Saint Petersburg 20ft $4,295 $3,886 $3,404 $4,738 22% 39% -14%
Yantian - Saint Petersburg 40ft / 40ft HC $5,806 $5,672 $4,625 $5,858 3% 27% -22%
Yantian - Istanbul 20ft $2,591 $2,342 $2,292 $3,472 48% 51% -33%
Yantian - Istanbul 40ft / 40ft HC $3,756 $3,273 $3,248 $4,809 47% 48% -33%
Yantian - Felixstowe 20ft $2,000 $1,935 $1,476 $2,129 10% 44% -55%
Yantian - Felixstowe 40ft / 40ft HC $3,003 $2,842 $2,332 $3,113 10% 33% -61%
Yantian - Genoa 20ft $2,804 $2,647 $2,356 $3,567 35% 51% -32%
Yantian - Genoa 40ft / 40ft HC $3,908 $3,754 $3,361 $5,091 36% 51% -31%
Colombo - Rotterdam 20ft $2,117 $1,730 $1,549 $1,830 6% 18% -43%
Colombo - Rotterdam 40ft / 40ft HC $2,335 $1,954 $1,794 $2,048 5% 14% -45%
Kaohsiung - Rotterdam 20ft $2,438 $1,771 $1,674 $2,455 39% 47% -51%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 11 June 2025


=== Page 12 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Kaohsiung - Rotterdam 40ft / 40ft HC $3,925 $2,698 $2,414 $3,450 28% 43% -57%
Kaohsiung - Felixstowe 20ft $1,959 $1,589 $1,558 $2,184 37% 40% -54%
Kaohsiung - Felixstowe 40ft / 40ft HC $3,249 $2,529 $2,321 $3,244 28% 40% -59%
Kaohsiung - Genoa 20ft $2,930 $2,458 $2,392 $3,719 51% 55% -33%
Kaohsiung - Genoa 40ft / 40ft HC $4,360 $3,579 $3,340 $5,260 47% 57% -31%
Laem Chabang - Rotterdam 20ft $1,871 $1,494 $1,674 $2,571 72% 54% -49%
Laem Chabang - Rotterdam 40ft / 40ft HC $3,094 $2,025 $2,618 $3,774 86% 44% -56%
Laem Chabang - Felixstowe 20ft $1,368 $1,518 $1,654 $2,536 67% 53% -56%
Laem Chabang - Felixstowe 40ft / 40ft HC $2,265 $2,272 $2,289 $3,922 73% 71% -59%
Laem Chabang - Genoa 20ft $2,397 $2,483 $2,765 $3,733 50% 35% -38%
Laem Chabang - Genoa 40ft / 40ft HC $3,382 $3,611 $3,858 $5,192 44% 35% -43%
Ho Chi Minh City - Rotterdam 20ft $2,117 $1,578 $1,454 $2,167 37% 49% -48%
Ho Chi Minh City - Rotterdam 40ft / 40ft HC $3,458 $2,471 $2,082 $3,226 31% 55% -55%
Ho Chi Minh City - Felixstowe 20ft $1,788 $1,705 $1,417 $1,906 12% 35% -57%
Ho Chi Minh City - Felixstowe 40ft / 40ft HC $2,992 $2,676 $2,159 $3,043 14% 41% -59%
Ho Chi Minh City - Genoa 20ft $2,966 $2,580 $2,556 $3,062 19% 20% -38%
Ho Chi Minh City - Genoa 40ft / 40ft HC $4,087 $3,466 $3,449 $4,217 22% 22% -41%
Shanghai - Port Said 20ft $2,922 $2,477 $2,597 $3,786 53% 46% -22%
Shanghai - Port Said 40ft / 40ft HC $3,656 $3,594 $3,756 $5,351 49% 42% -18%
Manila - Rotterdam 20ft $2,395 $1,586 $1,397 $2,395 51% 71% -45%
Manila - Rotterdam 40ft / 40ft HC $3,840 $2,566 $2,366 $3,622 41% 53% -49%
Manila - Felixstowe 20ft $1,865 $1,715 $1,351 $1,710 -0% 27% -69%
Manila - Felixstowe 40ft / 40ft HC $3,034 $2,739 $2,131 $2,477 -10% 16% -72%
Manila - Genoa 20ft $2,837 $2,812 $2,636 $2,982 6% 13% -47%
Manila - Genoa 40ft / 40ft HC $4,006 $3,904 $3,598 $4,067 4% 13% -48%
Singapore - Rotterdam 20ft $1,921 $1,728 $1,492 $2,203 27% 48% -47%
Singapore - Rotterdam 40ft / 40ft HC $2,908 $2,527 $2,193 $3,290 30% 50% -53%
Singapore - Felixstowe 20ft $1,617 $1,586 $1,400 $2,100 32% 50% -48%
Singapore - Felixstowe 40ft / 40ft HC $2,604 $2,512 $2,202 $3,214 28% 46% -53%
Singapore - Genoa 20ft $2,456 $2,320 $2,222 $2,662 15% 20% -45%
Singapore - Genoa 40ft / 40ft HC $3,544 $2,995 $2,900 $3,816 27% 32% -42%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 12 June 2025


=== Page 13 ===

Container Freight Rate | Insight
ASIA-EUROPE EB RATE INDEX (US$/40FT)
Backhaul rates to Asia-Europe EB Rate Index (US$/40ft)
$850
remain stable
In line with our expectations, Drewry’s Asia-Europe
$800
Eastbound Index increased a marginal $36 to reach $747
per 40ft container in June. Even though spot rates are 21%
lower YoY and 31% below 2019 levels, we expect them to
$750
remain stable next month.
According to the latest demand data, the multi-year
$700
decline in cargo volume from North Europe to China has
c
in
o n
th
ti
e
n u
s
e
a
d
m
w
e
i t
p
h
e
c
ri
a
o
r
d
g o
o f
v o
2
l
0
u
2
m
4
e
. C
be
o
i
m
ng
p a
4
r
%
ed
lo
to
w e
p
r
r e
in
v i
1
o
Q
us
2 5
y e
th
ar
a
s
n
, Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
1Q25 volumes were also down 22% from 2019, 21% from
2020 and 24% from 2021. The load factor fell to its lowest
level since 2015, reaching 34% in April, helping to explain Drewry Asia-Europe EB Rate Index (US$/40ft) Rate Index
History
the lower rates on the Asia–Europe backhaul trade.
Sep-24 $813
Several ocean ports in Northern Europe, specifically
Antwerp and Bremerhaven are experiencing delays due to Oct-24 $770 % change Sep 24 - Oct 24 -5%
worsening congestion, which escalated in April following a Nov-24 $737 % change Oct 24 - Nov 24 -4%
series of port strikes and lower-than-usual labour
Dec-24 $728 % change Nov 24 - Dec 24 -1%
availability ahead of the Easter holidays. As a result,
carriers are omitting port calls at the affected terminals to Jan-25 $722 % change Dec 24 - Jan 25 -1%
avoid disruptions. Feb-25 $723 % change Jan 25 - Feb 25 0%
Mar-25 $706 % change Feb 25 - Mar 25 -2%
Apr-25 $709 % change Mar 25 - Apr 25 0%
May-25 $711 % change Apr 25 - May 25 0%
Jun-25 $747 % change May 25 - Jun 25 5%
Asia-Europe EB Rate Index (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Rotterdam - Shanghai 20ft $540 $549 $540 $599 9% 11% -16%
Rotterdam - Shanghai 40ft / 40ft HC $609 $622 $643 $672 8% 5% -16%
Genoa - Shanghai 20ft $642 $628 $594 $627 -0% 6% -22%
Genoa - Shanghai 40ft / 40ft HC $806 $790 $750 $797 1% 6% -24%
Rotterdam - Yokohama 20ft $904 $904 $890 $900 -0% 1% -29%
Rotterdam - Yokohama 40ft / 40ft HC $1,184 $1,194 $1,130 $1,221 2% 8% -23%
Genoa - Yokohama 20ft $897 $826 $820 $846 2% 3% -30%
Genoa - Yokohama 40ft / 40ft HC $1,276 $1,069 $1,081 $1,075 1% -1% -38%
Rotterdam - Busan 20ft $484 $501 $518 $522 4% 1% -31%
Rotterdam - Busan 40ft / 40ft HC $619 $633 $645 $661 4% 2% -30%
Genoa - Busan 20ft $466 $454 $476 $496 9% 4% -28%
Genoa - Busan 40ft / 40ft HC $578 $550 $557 $582 6% 4% -34%
Port Said - Shanghai 20ft $615 $606 $606 $523 -14% -14% -39%
Port Said - Shanghai 40ft / 40ft HC $731 $701 $677 $658 -6% -3% -52%
Port Said - Tianjin 20ft $607 $600 $600 $517 -14% -14% -51%
Port Said - Tianjin 40ft / 40ft HC $701 $668 $668 $626 -6% -6% -55%
Port Said - Yantian 20ft $694 $672 $564 $621 -8% 10% -40%
Port Said - Yantian 40ft / 40ft HC $792 $655 $579 $575 -12% -1% -58%
Rotterdam - Hong Kong 20ft $646 $744 $683 $742 -0% 9% -17%
Rotterdam - Hong Kong 40ft / 40ft HC $738 $906 $843 $870 -4% 3% -21%
Rotterdam - Jakarta 20ft $565 $587 $612 $890 52% 45% -15%
Rotterdam - Jakarta 40ft / 40ft HC $686 $704 $728 $1,027 46% 41% -21%
Rotterdam - Tanjung Pelepas 20ft $699 $687 $496 $734 7% 48% -21%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 13 June 2025


=== Page 14 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Rotterdam - Tanjung Pelepas 40ft / 40ft HC $788 $778 $560 $828 6% 48% -23%
Rotterdam - Tianjin 20ft $473 $595 $677 $543 -9% -20% -15%
Rotterdam - Tianjin 40ft / 40ft HC $592 $742 $845 $614 -17% -27% -21%
Rotterdam - Manila 20ft $1,075 $1,101 $1,101 $1,352 23% 23% 30%
Rotterdam - Manila 40ft / 40ft HC $1,292 $1,438 $1,438 $1,690 18% 18% 28%
Rotterdam - Singapore 20ft $414 $438 $377 $586 34% 55% -16%
Rotterdam - Singapore 40ft / 40ft HC $529 $618 $518 $767 24% 48% -8%
Rotterdam - Yantian 20ft $385 $466 $488 $472 1% -3% -38%
Rotterdam - Yantian 40ft / 40ft HC $444 $514 $599 $525 2% -12% -46%
Rotterdam - Kaohsiung 20ft $518 $643 $628 $658 2% 5% -12%
Rotterdam - Kaohsiung 40ft / 40ft HC $613 $754 $732 $762 1% 4% -16%
Rotterdam - Laem Chabang 20ft $540 $492 $416 $652 33% 57% -30%
Rotterdam - Laem Chabang 40ft / 40ft HC $663 $620 $522 $761 23% 46% -41%
Rotterdam - Ho Chi Minh City 20ft $516 $358 $286 $274 -23% -4% -62%
Rotterdam - Ho Chi Minh City 40ft / 40ft HC $638 $444 $356 $378 -15% 6% -58%
Saint Petersburg - Shanghai 20ft $1,234 $1,479 $1,479 $1,499 1% 1% -29%
Saint Petersburg - Shanghai 40ft / 40ft HC $1,582 $2,292 $2,292 $2,332 2% 2% -18%
Saint Petersburg - Tianjin 20ft $1,230 $1,475 $1,135 $1,045 -29% -8% -55%
Saint Petersburg - Tianjin 40ft / 40ft HC $1,560 $2,270 $1,000 $1,860 -18% 86% -40%
Saint Petersburg - Yantian 20ft $1,158 $1,403 $913 $973 -31% 7% -59%
Saint Petersburg - Yantian 40ft / 40ft HC $1,457 $2,167 $1,122 $1,757 -19% 57% -44%
Istanbul - Shanghai 20ft $692 $686 $656 $628 -8% -4% -20%
Istanbul - Shanghai 40ft / 40ft HC $892 $870 $834 $797 -8% -4% -21%
Istanbul - Tianjin 20ft $730 $687 $577 $543 -21% -6% -39%
Istanbul - Tianjin 40ft / 40ft HC $950 $824 $670 $754 -8% 13% -35%
Istanbul - Yantian 20ft $761 $665 $504 $509 -23% 1% -44%
Istanbul - Yantian 40ft / 40ft HC $982 $757 $711 $721 -5% 1% -40%
Felixstowe - Shanghai 20ft $399 $398 $388 $422 6% 9% -43%
Felixstowe - Shanghai 40ft / 40ft HC $473 $481 $473 $484 1% 2% -41%
Felixstowe - Hong Kong 20ft $595 $643 $637 $669 4% 5% -24%
Felixstowe - Hong Kong 40ft / 40ft HC $718 $814 $754 $838 3% 11% -20%
Felixstowe - Yokohama 20ft $745 $749 $788 $877 17% 11% -27%
Felixstowe - Yokohama 40ft / 40ft HC $1,026 $1,065 $1,081 $1,159 9% 7% -21%
Felixstowe - Busan 20ft $563 $563 $555 $764 36% 38% -2%
Felixstowe - Busan 40ft / 40ft HC $728 $805 $748 $1,024 27% 37% 5%
Felixstowe - Tianjin 20ft $698 $656 $481 $482 -27% 0% -35%
Felixstowe - Tianjin 40ft / 40ft HC $746 $757 $644 $633 -16% -2% -31%
Felixstowe - Manila 20ft $1,070 $1,071 $1,071 $1,149 7% 7% -12%
Felixstowe - Manila 40ft / 40ft HC $1,364 $1,536 $1,553 $1,532 -0% -1% 0%
Felixstowe - Singapore 20ft $363 $371 $411 $420 13% 2% -42%
Felixstowe - Singapore 40ft / 40ft HC $475 $522 $560 $536 3% -4% -41%
Felixstowe - Yantian 20ft $368 $360 $335 $396 10% 18% -49%
Felixstowe - Yantian 40ft / 40ft HC $434 $438 $408 $443 1% 9% -50%
Felixstowe - Kaohsiung 20ft $552 $517 $506 $706 37% 40% -11%
Felixstowe - Kaohsiung 40ft / 40ft HC $671 $623 $617 $826 33% 34% -10%
Felixstowe - Laem Chabang 20ft $568 $644 $510 $617 -4% 21% -40%
Felixstowe - Laem Chabang 40ft / 40ft HC $671 $760 $605 $757 -0% 25% -42%
Felixstowe - Ho Chi Minh City 20ft $510 $470 $452 $577 23% 28% -28%
Felixstowe - Ho Chi Minh City 40ft / 40ft HC $672 $656 $642 $730 11% 14% -30%
Genoa - Hong Kong 20ft $617 $620 $653 $700 13% 7% -23%
Genoa - Hong Kong 40ft / 40ft HC $751 $756 $792 $894 18% 13% -21%
Genoa - Jakarta 20ft $545 $602 $642 $649 8% 1% -16%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 14 June 2025


=== Page 15 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Genoa - Jakarta 40ft / 40ft HC $685 $717 $740 $762 6% 3% -24%
Genoa - Tanjung Pelepas 20ft $819 $788 $818 $788 0% -4% -22%
Genoa - Tanjung Pelepas 40ft / 40ft HC $1,018 $914 $956 $906 -1% -5% -32%
Genoa - Tianjin 20ft $538 $532 $542 $508 -5% -6% -28%
Genoa - Tianjin 40ft / 40ft HC $650 $657 $643 $547 -17% -15% -38%
Genoa - Manila 20ft $940 $1,026 $1,100 $1,093 7% -1% -16%
Genoa - Manila 40ft / 40ft HC $1,224 $1,297 $1,400 $1,372 6% -2% -15%
Genoa - Singapore 20ft $418 $455 $478 $479 5% 0% -30%
Genoa - Singapore 40ft / 40ft HC $548 $571 $603 $609 7% 1% -32%
Genoa - Yantian 20ft $515 $509 $527 $528 4% 0% -22%
Genoa - Yantian 40ft / 40ft HC $615 $611 $605 $615 1% 2% -26%
Genoa - Kaohsiung 20ft $606 $599 $623 $728 22% 17% -13%
Genoa - Kaohsiung 40ft / 40ft HC $731 $733 $768 $885 21% 15% -13%
Genoa - Laem Chabang 20ft $681 $767 $649 $745 -3% 15% -26%
Genoa - Laem Chabang 40ft / 40ft HC $860 $1,143 $800 $898 -21% 12% -34%
Genoa - Ho Chi Minh City 20ft $600 $580 $572 $681 17% 19% -26%
Genoa - Ho Chi Minh City 40ft / 40ft HC $860 $732 $718 $810 11% 13% -35%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 15 June 2025


=== Page 16 ===

Container Freight Rate | Insight
INTRA-ASIA FREIGHT RATE INDEX (US$/40FT)
Intra-Asia rates remain Intra-Asia Freight Rate Index (US$/40ft)
$1,050
stable
$1,000
Drewry’s key Intra-Asia Freight Rate Index rose 5% in June
to $957 per 40ft container as rates were 2% higher than in
June 2024 and remained 17% above pre-pandemic levels. $950
We expect intra-Asia spot rates to remain stable in July.
$900
China's manufacturing sector held steady in May 2025,
with a PMI of 49.5. Sustained demand from Southeast Asia
$850
drove an increase in intra-Asian cargo shipments. The
l
d
a
e
t
m
es
a
t
n
d
d
e m
b
a
y
n d
1
fi
4
g
%
u res
Y o
(
Y
M
.
a
H
y
o
)
w
a
e
l
v
s
e
o
r ,
r ep
p
o
o
r
r
t
t
e d
c o
a
n
n
g e
u
s
p
ti
t
o
ic
n
k i
i
n
n Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
Southeast Asia—especially at Singapore and Port Klang—is
causing unreliable sailing schedules and unpredictable
transit times for cargo. Drewry Intra-Asia Freight Rate Index (US$/40ft) Rate Index
History
In line with the index, rates on the Shanghai-Laem
Sep-24 $908
Chabang route increased 2%, reaching $1,230 per 40ft
container, while those on the Shanghai-Busan route Oct-24 $886 % change Sep 24 - Oct 24 -2%
increased 2% in June, to $851 per 40ft container. Nov-24 $1,003 % change Oct 24 - Nov 24 13%
Dec-24 $975 % change Nov 24 - Dec 24 -3%
Jan-25 $889 % change Dec 24 - Jan 25 -9%
Feb-25 $855 % change Jan 25 - Feb 25 -4%
Mar-25 $883 % change Feb 25 - Mar 25 3%
Apr-25 $924 % change Mar 25 - Apr 25 5%
May-25 $911 % change Apr 25 - May 25 -1%
Jun-25 $957 % change May 25 - Jun 25 5%
Intra-Asia Freight Rate Index (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Shanghai - Yokohama 20ft $841 $867 $828 $847 -2% 2% 24%
Shanghai - Yokohama 40ft / 40ft HC $1,410 $1,427 $1,372 $1,368 -4% -0% 21%
Shanghai - Busan 20ft $437 $474 $497 $501 6% 1% 3%
Shanghai - Busan 40ft / 40ft HC $739 $799 $833 $851 7% 2% 8%
Shanghai - Laem Chabang 20ft $593 $736 $672 $721 -2% 7% -0%
Shanghai - Laem Chabang 40ft / 40ft HC $1,054 $1,262 $1,202 $1,230 -3% 2% -9%
Hong Kong - Shanghai 20ft $498 $516 $519 $599 16% 15% -6%
Hong Kong - Shanghai 40ft / 40ft HC $709 $727 $724 $835 15% 15% -11%
Hong Kong - Yokohama 20ft $672 $673 $676 $688 2% 2% -9%
Hong Kong - Yokohama 40ft / 40ft HC $1,115 $1,123 $1,047 $1,110 -1% 6% -2%
Hong Kong - Busan 20ft $479 $577 $533 $521 -10% -2% -12%
Hong Kong - Busan 40ft / 40ft HC $762 $887 $810 $795 -10% -2% -12%
Yokohama - Shanghai 20ft $349 $338 $396 $453 34% 14% 50%
Yokohama - Shanghai 40ft / 40ft HC $543 $520 $581 $691 33% 19% 47%
Yokohama - Hong Kong 20ft $586 $582 $576 $619 6% 7% -9%
Yokohama - Hong Kong 40ft / 40ft HC $970 $965 $948 $988 2% 4% -6%
Yokohama - Busan 20ft $552 $553 $585 $568 3% -3% -21%
Yokohama - Busan 40ft / 40ft HC $882 $885 $894 $892 1% -0% -18%
Yokohama - Laem Chabang 20ft $667 $641 $662 $768 20% 16% -19%
Yokohama - Laem Chabang 40ft / 40ft HC $1,078 $1,011 $1,076 $1,338 32% 24% -19%
Busan - Shanghai 20ft $281 $280 $277 $285 2% 3% -4%
Busan - Shanghai 40ft / 40ft HC $430 $429 $422 $435 1% 3% -5%
Busan - Yokohama 20ft $574 $575 $620 $655 14% 6% 3%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 16 June 2025


=== Page 17 ===

Container Freight Rate | Insight
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Busan - Yokohama 40ft / 40ft HC $950 $998 $1,016 $1,116 12% 10% 2%
Laem Chabang - Shanghai 20ft $367 $364 $336 $360 -1% 7% -12%
Laem Chabang - Shanghai 40ft / 40ft HC $514 $527 $498 $521 -1% 5% -10%
Laem Chabang - Yokohama 20ft $672 $709 $631 $657 -7% 4% -14%
Laem Chabang - Yokohama 40ft / 40ft HC $963 $948 $939 $1,064 12% 13% -7%
Yokohama - Tianjin 20ft $602 $602 $599 $602 0% 1% -8%
Yokohama - Tianjin 40ft / 40ft HC $904 $904 $890 $904 0% 2% 3%
Shanghai - Hong Kong 20ft $572 $626 $705 $664 6% -6% 34%
Shanghai - Hong Kong 40ft / 40ft HC $930 $1,026 $1,230 $1,114 9% -9% 32%
Shanghai - Jakarta 20ft $883 $1,024 $896 $820 -20% -8% -18%
Shanghai - Jakarta 40ft / 40ft HC $1,608 $1,895 $1,616 $1,458 -23% -10% -15%
Shanghai - Tanjung Pelepas 20ft $837 $848 $794 $824 -3% 4% -21%
Shanghai - Tanjung Pelepas 40ft / 40ft HC $1,397 $1,425 $1,386 $1,394 -2% 1% -17%
Shanghai - Manila 20ft $468 $393 $358 $363 -8% 1% -23%
Shanghai - Manila 40ft / 40ft HC $746 $596 $517 $554 -7% 7% -23%
Shanghai - Singapore 20ft $602 $589 $669 $708 20% 6% -25%
Shanghai - Singapore 40ft / 40ft HC $1,071 $1,074 $1,189 $1,246 16% 5% -27%
Shanghai - Kaohsiung 20ft $918 $979 $951 $932 -5% -2% 97%
Shanghai - Kaohsiung 40ft / 40ft HC $1,556 $1,710 $1,677 $1,662 -3% -1% 133%
Shanghai - Ho Chi Minh City 20ft $545 $682 $676 $703 3% 4% 11%
Shanghai - Ho Chi Minh City 40ft / 40ft HC $990 $1,222 $1,222 $1,272 4% 4% 10%
Hong Kong - Tianjin 20ft $459 $522 $497 $552 6% 11% 3%
Hong Kong - Tianjin 40ft / 40ft HC $659 $745 $708 $785 5% 11% -2%
Jakarta - Shanghai 20ft $235 $239 $263 $271 13% 3% -6%
Jakarta - Shanghai 40ft / 40ft HC $383 $394 $414 $438 11% 6% -11%
Jakarta - Yokohama 20ft $682 $637 $675 $714 12% 6% -7%
Jakarta - Yokohama 40ft / 40ft HC $1,051 $989 $1,095 $1,167 18% 7% -3%
Yokohama - Jakarta 20ft $796 $801 $829 $927 16% 12% 15%
Yokohama - Jakarta 40ft / 40ft HC $1,386 $1,392 $1,431 $1,645 18% 15% 21%
Yokohama - Singapore 20ft $962 $896 $872 $815 -9% -7% 20%
Yokohama - Singapore 40ft / 40ft HC $1,621 $1,512 $1,446 $1,390 -8% -4% 25%
Yokohama - Yantian 20ft $546 $593 $654 $619 4% -5% 16%
Yokohama - Yantian 40ft / 40ft HC $899 $984 $1,014 $994 1% -2% 17%
Yokohama - Kaohsiung 20ft $429 $432 $427 $498 15% 17% 34%
Yokohama - Kaohsiung 40ft / 40ft HC $671 $640 $630 $727 14% 15% 36%
Busan - Hong Kong 20ft $433 $510 $539 $506 -1% -6% 27%
Busan - Hong Kong 40ft / 40ft HC $614 $680 $775 $721 6% -7% 27%
Busan - Tianjin 20ft $410 $356 $339 $328 -8% -3% 2%
Busan - Tianjin 40ft / 40ft HC $569 $515 $482 $454 -12% -6% -9%
Busan - Singapore 20ft $849 $890 $853 $946 6% 11% 32%
Busan - Singapore 40ft / 40ft HC $1,451 $1,494 $1,428 $1,554 4% 9% 32%
Busan - Yantian 20ft $475 $455 $438 $486 7% 11% 20%
Busan - Yantian 40ft / 40ft HC $766 $748 $732 $794 6% 8% 20%
Tanjung Pelepas - Shanghai 20ft $497 $362 $404 $432 19% 7% 25%
Tanjung Pelepas - Shanghai 40ft / 40ft HC $672 $592 $644 $677 14% 5% 28%
Tanjung Pelepas - Hong Kong 20ft $397 $387 $428 $677 75% 58% 38%
Tanjung Pelepas - Hong Kong 40ft / 40ft HC $610 $600 $665 $948 58% 43% 30%
Tanjung Pelepas - Tianjin 20ft $465 $432 $440 $448 4% 2% -10%
Tanjung Pelepas - Tianjin 40ft / 40ft HC $699 $649 $657 $680 5% 4% 7%
Tanjung Pelepas - Yantian 20ft $546 $406 $431 $422 4% -2% -6%
Tanjung Pelepas - Yantian 40ft / 40ft HC $737 $642 $666 $647 1% -3% -1%
Tanjung Pelepas - Kaohsiung 20ft $381 $385 $385 $608 58% 58% 27%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 17 June 2025


=== Page 18 ===

Container Freight Rate | Insight
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Tanjung Pelepas - Kaohsiung 40ft / 40ft HC $628 $633 $633 $993 57% 57% 30%
Tianjin - Hong Kong 20ft $603 $720 $753 $716 -1% -5% 21%
Tianjin - Hong Kong 40ft / 40ft HC $788 $976 $1,003 $942 -3% -6% 10%
Tianjin - Yokohama 20ft $682 $657 $625 $670 2% 7% -7%
Tianjin - Yokohama 40ft / 40ft HC $1,055 $988 $940 $1,018 3% 8% 8%
Tianjin - Busan 20ft $510 $456 $538 $467 2% -13% -6%
Tianjin - Busan 40ft / 40ft HC $626 $600 $662 $611 2% -8% -3%
Tianjin - Tanjung Pelepas 20ft $1,221 $1,208 $1,371 $1,175 -3% -14% 7%
Tianjin - Tanjung Pelepas 40ft / 40ft HC $1,586 $1,505 $1,805 $1,393 -7% -23% -21%
Tianjin - Manila 20ft $647 $630 $591 $670 6% 13% 21%
Tianjin - Manila 40ft / 40ft HC $806 $747 $673 $697 -7% 4% -13%
Tianjin - Singapore 20ft $1,358 $1,092 $937 $849 -22% -9% -18%
Tianjin - Singapore 40ft / 40ft HC $1,798 $1,348 $1,220 $1,198 -11% -2% -20%
Tianjin - Kaohsiung 20ft $848 $968 $1,015 $977 1% -4% 74%
Tianjin - Kaohsiung 40ft / 40ft HC $1,258 $1,292 $1,370 $1,293 0% -6% 54%
Tianjin - Laem Chabang 20ft $992 $964 $953 $950 -1% -0% -9%
Tianjin - Laem Chabang 40ft / 40ft HC $1,222 $1,201 $1,151 $1,166 -3% 1% -29%
Tianjin - Ho Chi Minh City 20ft $775 $1,003 $1,091 $980 -2% -10% 9%
Tianjin - Ho Chi Minh City 40ft / 40ft HC $1,139 $1,259 $1,473 $1,354 8% -8% 10%
Manila - Shanghai 20ft $619 $502 $514 $546 9% 6% 9%
Manila - Shanghai 40ft / 40ft HC $918 $777 $795 $818 5% 3% 20%
Manila - Tianjin 20ft $645 $529 $552 $612 16% 11% 20%
Manila - Tianjin 40ft / 40ft HC $977 $836 $860 $896 7% 4% 22%
Manila - Yantian 20ft $700 $704 $700 $671 -5% -4% 31%
Manila - Yantian 40ft / 40ft HC $1,071 $1,139 $1,113 $1,089 -4% -2% 49%
Singapore - Shanghai 20ft $403 $418 $364 $400 -4% 10% -3%
Singapore - Shanghai 40ft / 40ft HC $600 $615 $531 $579 -6% 9% -6%
Singapore - Yokohama 20ft $849 $850 $849 $904 6% 6% 2%
Singapore - Yokohama 40ft / 40ft HC $1,309 $1,311 $1,328 $1,440 10% 8% 6%
Singapore - Busan 20ft $334 $364 $392 $469 29% 20% -22%
Singapore - Busan 40ft / 40ft HC $531 $564 $596 $719 27% 21% -25%
Singapore - Tanjung Pelepas 20ft $386 $338 $344 $266 -21% -23% -56%
Singapore - Tanjung Pelepas 40ft / 40ft HC $595 $524 $530 $421 -20% -21% -57%
Singapore - Tianjin 20ft $530 $559 $476 $482 -14% 1% -8%
Singapore - Tianjin 40ft / 40ft HC $826 $852 $654 $667 -22% 2% -16%
Singapore - Manila 20ft $573 $524 $645 $772 47% 20% 29%
Singapore - Manila 40ft / 40ft HC $973 $813 $1,011 $1,244 53% 23% 15%
Singapore - Yantian 20ft $422 $451 $423 $535 19% 26% -5%
Singapore - Yantian 40ft / 40ft HC $612 $638 $553 $725 14% 31% -9%
Singapore - Kaohsiung 20ft $467 $477 $456 $521 9% 14% -14%
Singapore - Kaohsiung 40ft / 40ft HC $711 $715 $661 $758 6% 15% -21%
Singapore - Laem Chabang 20ft $225 $214 $230 $136 -36% -41% -71%
Singapore - Laem Chabang 40ft / 40ft HC $420 $411 $411 $274 -33% -33% -62%
Yantian - Yokohama 20ft $815 $803 $827 $791 -1% -4% 15%
Yantian - Yokohama 40ft / 40ft HC $1,387 $1,341 $1,367 $1,270 -5% -7% 16%
Yantian - Busan 20ft $477 $504 $510 $470 -7% -8% 12%
Yantian - Busan 40ft / 40ft HC $830 $870 $876 $803 -8% -8% 21%
Yantian - Tanjung Pelepas 20ft $1,086 $979 $953 $906 -7% -5% 2%
Yantian - Tanjung Pelepas 40ft / 40ft HC $1,841 $1,710 $1,717 $1,648 -4% -4% 17%
Yantian - Manila 20ft $462 $412 $416 $475 15% 14% 0%
Yantian - Manila 40ft / 40ft HC $734 $602 $608 $752 25% 24% -2%
Yantian - Singapore 20ft $698 $668 $695 $689 3% -1% -24%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 18 June 2025


=== Page 19 ===

Container Freight Rate | Insight
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Yantian - Singapore 40ft / 40ft HC $1,220 $1,170 $1,121 $1,099 -6% -2% -32%
Yantian - Kaohsiung 20ft $748 $722 $722 $685 -5% -5% 50%
Yantian - Kaohsiung 40ft / 40ft HC $1,215 $1,196 $1,196 $1,141 -5% -5% 63%
Yantian - Laem Chabang 20ft $494 $622 $514 $467 -25% -9% -32%
Yantian - Laem Chabang 40ft / 40ft HC $869 $1,010 $779 $674 -33% -13% -43%
Yantian - Ho Chi Minh City 20ft $456 $515 $505 $507 -2% 0% -18%
Yantian - Ho Chi Minh City 40ft / 40ft HC $778 $878 $834 $876 -0% 5% -16%
Kaohsiung - Shanghai 20ft $408 $442 $450 $464 5% 3% 22%
Kaohsiung - Shanghai 40ft / 40ft HC $547 $580 $577 $600 3% 4% 16%
Kaohsiung - Yokohama 20ft $438 $482 $513 $559 16% 9% 16%
Kaohsiung - Yokohama 40ft / 40ft HC $669 $711 $718 $821 15% 14% 18%
Kaohsiung - Tianjin 20ft $369 $408 $508 $572 40% 13% 77%
Kaohsiung - Tianjin 40ft / 40ft HC $514 $551 $651 $730 32% 12% 71%
Kaohsiung - Yantian 20ft $399 $405 $405 $462 14% 14% 31%
Kaohsiung - Yantian 40ft / 40ft HC $517 $541 $541 $614 13% 13% 36%
Kaohsiung - Laem Chabang 20ft $715 $728 $680 $720 -1% 6% 70%
Kaohsiung - Laem Chabang 40ft / 40ft HC $1,284 $1,324 $1,216 $1,254 -5% 3% 110%
Kaohsiung - Ho Chi Minh City 20ft $392 $380 $377 $452 19% 20% 23%
Kaohsiung - Ho Chi Minh City 40ft / 40ft HC $574 $552 $532 $645 17% 21% 30%
Laem Chabang - Tianjin 20ft $490 $503 $513 $558 11% 9% 30%
Laem Chabang - Tianjin 40ft / 40ft HC $713 $690 $720 $826 20% 15% 31%
Laem Chabang - Yantian 20ft $543 $526 $649 $624 19% -4% 32%
Laem Chabang - Yantian 40ft / 40ft HC $775 $747 $899 $873 17% -3% 19%
Ho Chi Minh City - Shanghai 20ft $262 $265 $261 $265 0% 2% -2%
Ho Chi Minh City - Shanghai 40ft / 40ft HC $394 $397 $386 $390 -2% 1% -6%
Ho Chi Minh City - Tianjin 20ft $350 $298 $264 $294 -1% 11% 8%
Ho Chi Minh City - Tianjin 40ft / 40ft HC $504 $450 $388 $408 -9% 5% 4%
Ho Chi Minh City - Yantian 20ft $434 $291 $280 $286 -2% 2% -11%
Ho Chi Minh City - Yantian 40ft / 40ft HC $679 $460 $435 $441 -4% 1% -13%
Yokohama - Ho Chi Minh City 20ft $834 $777 $692 $765 -2% 11% 13%
Yokohama - Ho Chi Minh City 40ft / 40ft HC $1,528 $1,316 $1,200 $1,216 -8% 1% 4%
Busan - Ho Chi Minh City 20ft $792 $781 $875 $769 -2% -12% 22%
Busan - Ho Chi Minh City 40ft / 40ft HC $1,350 $1,300 $1,451 $1,231 -5% -15% 14%
Manila - Ho Chi Minh City 20ft $521 $464 $614 $519 12% -15% -28%
Manila - Ho Chi Minh City 40ft / 40ft HC $870 $734 $944 $837 14% -11% -31%
Laem Chabang - Ho Chi Minh City 20ft $329 $370 $362 $355 -4% -2% -4%
Laem Chabang - Ho Chi Minh City 40ft / 40ft HC $541 $670 $594 $525 -22% -12% -15%
Ho Chi Minh City - Manila 20ft $627 $615 $669 $717 17% 7% 17%
Ho Chi Minh City - Manila 40ft / 40ft HC $1,128 $1,065 $1,155 $1,224 15% 6% 17%
Ho Chi Minh City - Yokohama 20ft $621 $731 $810 $641 -12% -21% 22%
Ho Chi Minh City - Yokohama 40ft / 40ft HC $1,016 $1,196 $1,266 $1,009 -16% -20% 21%
Ho Chi Minh City - Laem Chabang 20ft $310 $461 $487 $351 -24% -28% 9%
Ho Chi Minh City - Laem Chabang 40ft / 40ft HC $522 $704 $738 $558 -21% -24% 2%
Ho Chi Minh City - Busan 20ft $501 $576 $583 $545 -5% -7% 44%
Ho Chi Minh City - Busan 40ft / 40ft HC $821 $903 $928 $810 -10% -13% 30%
Ho Chi Minh City - Tanjung Pelepas 20ft $526 $607 $699 $787 30% 13% 76%
Ho Chi Minh City - Tanjung Pelepas 40ft / 40ft HC $923 $1,053 $1,253 $1,299 23% 4% 67%
Ho Chi Minh City - Kaohsiung 20ft $474 $519 $551 $525 1% -5% 42%
Ho Chi Minh City - Kaohsiung 40ft / 40ft HC $731 $773 $827 $726 -6% -12% 33%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 19 June 2025


=== Page 20 ===

Container Freight Rate | Insight
SOUTH CHINA-DUBAI BENCHMARK (US$/40FT)
Rates likely to South China-Dubai Benchmark (US$/40ft)
$3,000
increase in July
Drewry's key benchmark for the South China to Dubai
$2,500
route shot up 22% MoM in June, reaching $2,083 per 40ft
container. This marks a 59% decline compared to the same
period last year. Rates increased substantially to 21%
$2,000
higher than pre-pandemic levels in 2019, and Drewry
expects them to increase next month as well.
$1,500
The ongoing conflict between Israel and Iran has led to
h
h
i
e
g
s
h
it
e
a
r
n t
f
t
r
o
e ig
c
h
o
t
v er
r a
s
t
h
e
i
s
p
.
m e
M
n
a
t
n
s
y
o n
i n
t
s
h
u
is
r a
r
n
o
c
u
e
t e,
c
a
o
n
m
d
p a
th
n
o
ie
s
s
e t
a
h
r
a
e
t Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
do have substantially increased their premiums, resulting
in higher surcharges.
Drewry South China-Dubai Benchmark (US$/40ft) Rate
Several routes experienced notable rate increases in June. Index History
For instance, rates on the Tianjin to Jebel Ali route
Sep-24 $2,894
increased 54% to $2,490 per 40ft container, while those on
the Tianjin to Dammam route increased 45% to $3,008 per Oct-24 $2,250 % change Sep 24 - Oct 24 -22%
40ft container. Nov-24 $2,417 % change Oct 24 - Nov 24 7%
Dec-24 $2,482 % change Nov 24 - Dec 24 3%
Jan-25 $2,490 % change Dec 24 - Jan 25 0%
Feb-25 $1,692 % change Jan 25 - Feb 25 -32%
Mar-25 $1,625 % change Feb 25 - Mar 25 -4%
Apr-25 $1,741 % change Mar 25 - Apr 25 7%
May-25 $1,713 % change Apr 25 - May 25 -2%
Jun-25 $2,083 % change May 25 - Jun 25 22%
South China-Dubai Benchmark (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Yantian - Jebel Ali 20ft $1,316 $1,354 $1,267 $1,477 9% 17% -59%
Yantian - Jebel Ali 40ft / 40ft HC $1,625 $1,741 $1,713 $2,083 20% 22% -59%
Yantian - Dammam 20ft $1,457 $1,598 $1,584 $2,426 52% 53% -26%
Yantian - Dammam 40ft / 40ft HC $2,004 $2,258 $2,048 $3,029 34% 48% -31%
Shanghai - Dammam 20ft $1,450 $1,708 $1,448 $2,653 55% 83% -19%
Shanghai - Dammam 40ft / 40ft HC $1,764 $2,092 $1,772 $3,103 48% 75% -31%
Shanghai - Jebel Ali 20ft $1,247 $1,516 $1,460 $2,294 51% 57% -29%
Shanghai - Jebel Ali 40ft / 40ft HC $1,514 $1,981 $1,843 $2,864 45% 55% -40%
Tianjin - Jebel Ali 20ft $1,410 $1,460 $1,494 $2,086 43% 40% -35%
Tianjin - Jebel Ali 40ft / 40ft HC $1,755 $1,875 $1,618 $2,490 33% 54% -46%
Tianjin - Dammam 20ft $1,549 $1,874 $1,702 $2,378 27% 40% -28%
Tianjin - Dammam 40ft / 40ft HC $1,832 $2,321 $2,076 $3,008 30% 45% -32%
Hong Kong - Jebel Ali 20ft $1,379 $1,662 $1,669 $2,372 43% 42% -34%
Hong Kong - Jebel Ali 40ft / 40ft HC $1,678 $2,281 $2,221 $3,152 38% 42% -34%
Yokohama - Dammam 20ft $2,216 $2,220 $2,098 $2,294 3% 9% -28%
Yokohama - Dammam 40ft / 40ft HC $3,032 $2,962 $2,767 $3,060 3% 11% -29%
Yokohama - Jebel Ali 20ft $2,060 $2,526 $2,381 $2,535 0% 6% -32%
Yokohama - Jebel Ali 40ft / 40ft HC $2,625 $3,288 $3,200 $3,496 6% 9% -29%
Busan - Dammam 20ft $1,466 $1,624 $1,502 $1,867 15% 24% -32%
Busan - Dammam 40ft / 40ft HC $1,965 $2,167 $1,997 $2,462 14% 23% -39%
Busan - Jebel Ali 20ft $1,455 $1,505 $1,510 $1,900 26% 26% -33%
Busan - Jebel Ali 40ft / 40ft HC $1,959 $2,015 $2,023 $2,489 24% 23% -38%
Singapore - Jebel Ali 20ft $1,367 $1,429 $1,452 $1,851 30% 27% -18%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 20 June 2025


=== Page 21 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Singapore - Jebel Ali 40ft / 40ft HC $1,813 $1,862 $1,884 $2,416 30% 28% -25%
Toronto via Montreal - Jawaharlal Nehru Port 20ft $2,472 $2,589 $2,592 $2,717 5% 5% 50%
Toronto via Montreal - Jawaharlal Nehru Port 40ft / 40ft HC $3,251 $3,408 $3,681 $3,846 13% 4% 68%
Toronto via Montreal - Jebel Ali 20ft $2,418 $2,792 $2,567 $2,460 -12% -4% 20%
Toronto via Montreal - Jebel Ali 40ft / 40ft HC $3,412 $3,862 $3,615 $3,602 -7% -0% 41%
Halifax - Jawaharlal Nehru Port 20ft $1,679 $1,815 $1,746 $1,846 2% 6% 7%
Halifax - Jawaharlal Nehru Port 40ft / 40ft HC $2,568 $2,789 $2,663 $2,732 -2% 3% -0%
Halifax - Jeddah 20ft $2,879 $3,013 $2,826 $2,896 -4% 2% 16%
Halifax - Jeddah 40ft / 40ft HC $3,940 $4,100 $3,956 $4,009 -2% 1% 23%
Halifax - Jebel Ali 20ft $2,447 $2,549 $2,405 $2,512 -1% 4% 28%
Halifax - Jebel Ali 40ft / 40ft HC $3,528 $3,617 $3,376 $3,501 -3% 4% 25%
Montreal - Jawaharlal Nehru Port 20ft $2,137 $2,193 $2,060 $2,390 9% 16% 35%
Montreal - Jawaharlal Nehru Port 40ft / 40ft HC $2,830 $3,205 $3,050 $3,438 7% 13% 51%
Montreal - Jeddah 20ft $3,410 $3,411 $3,226 $2,782 -18% -14% 7%
Montreal - Jeddah 40ft / 40ft HC $4,594 $4,521 $4,389 $3,522 -22% -20% 4%
Montreal - Jebel Ali 20ft $2,162 $2,441 $2,258 $2,370 -3% 5% 26%
Montreal - Jebel Ali 40ft / 40ft HC $2,872 $3,511 $3,275 $3,392 -3% 4% 39%
Vancouver - Jawaharlal Nehru Port 20ft $2,236 $2,503 $2,365 $2,689 7% 14% 29%
Vancouver - Jawaharlal Nehru Port 40ft / 40ft HC $3,676 $3,778 $3,567 $3,952 5% 11% 30%
Vancouver - Jeddah 20ft $5,060 $5,061 $4,874 $5,064 0% 4% 42%
Vancouver - Jeddah 40ft / 40ft HC $7,336 $7,230 $7,019 $7,227 -0% 3% 44%
Vancouver - Jebel Ali 20ft $3,241 $3,242 $3,031 $3,405 5% 12% 27%
Vancouver - Jebel Ali 40ft / 40ft HC $5,097 $5,085 $4,778 $5,219 3% 9% 26%
Shanghai - Jawaharlal Nehru Port 20ft $1,065 $1,129 $1,077 $2,063 83% 92% -47%
Shanghai - Jawaharlal Nehru Port 40ft / 40ft HC $1,202 $1,273 $1,286 $2,271 78% 77% -46%
Shanghai - Ashdod 20ft $2,705 $2,212 $2,424 $3,682 66% 52% -21%
Shanghai - Ashdod 40ft / 40ft HC $3,585 $3,223 $3,586 $5,305 65% 48% -9%
Hong Kong - Jawaharlal Nehru Port 20ft $1,261 $1,340 $1,332 $2,736 104% 105% -30%
Hong Kong - Jawaharlal Nehru Port 40ft / 40ft HC $1,468 $1,516 $1,496 $3,004 98% 101% -30%
Jawaharlal Nehru Port - Toronto via Montreal 20ft $4,062 $3,502 $3,494 $3,770 8% 8% -23%
Jawaharlal Nehru Port - Toronto via Montreal 40ft / 40ft HC $4,545 $4,110 $3,928 $4,366 6% 11% -24%
Jawaharlal Nehru Port - Halifax 20ft $3,310 $3,213 $3,247 $3,621 13% 12% -19%
Jawaharlal Nehru Port - Halifax 40ft / 40ft HC $3,671 $3,442 $3,539 $3,988 16% 13% -21%
Jawaharlal Nehru Port - Vancouver 20ft $3,649 $2,626 $2,814 $3,301 26% 17% -34%
Jawaharlal Nehru Port - Vancouver 40ft / 40ft HC $4,308 $3,202 $3,295 $3,981 24% 21% -32%
Jawaharlal Nehru Port - Shanghai 20ft $267 $267 $264 $272 2% 3% -3%
Jawaharlal Nehru Port - Shanghai 40ft / 40ft HC $392 $391 $386 $399 2% 3% -1%
Jawaharlal Nehru Port - Hong Kong 20ft $389 $389 $394 $400 3% 2% -23%
Jawaharlal Nehru Port - Hong Kong 40ft / 40ft HC $540 $538 $544 $561 4% 3% -15%
Jawaharlal Nehru Port - Yokohama 20ft $734 $639 $581 $710 11% 22% 13%
Jawaharlal Nehru Port - Yokohama 40ft / 40ft HC $1,022 $877 $841 $948 8% 13% 8%
Jawaharlal Nehru Port - Busan 20ft $202 $240 $260 $263 10% 1% 4%
Jawaharlal Nehru Port - Busan 40ft / 40ft HC $291 $333 $376 $392 18% 4% -2%
Jawaharlal Nehru Port - Tianjin 20ft $304 $300 $285 $304 1% 7% 2%
Jawaharlal Nehru Port - Tianjin 40ft / 40ft HC $443 $479 $439 $463 -3% 5% 2%
Jawaharlal Nehru Port - Rotterdam 20ft $2,187 $1,766 $1,532 $1,955 11% 28% -42%
Jawaharlal Nehru Port - Rotterdam 40ft / 40ft HC $2,429 $1,963 $1,682 $2,118 8% 26% -40%
Jawaharlal Nehru Port - Dammam 20ft $762 $725 $702 $709 -2% 1% -26%
Jawaharlal Nehru Port - Dammam 40ft / 40ft HC $1,065 $1,019 $1,000 $1,137 12% 14% -6%
Jawaharlal Nehru Port - Singapore 20ft $306 $306 $306 $318 4% 4% -2%
Jawaharlal Nehru Port - Singapore 40ft / 40ft HC $452 $453 $449 $466 3% 4% -1%
Jawaharlal Nehru Port - Yantian 20ft $296 $317 $314 $294 -7% -6% -4%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 21 June 2025


=== Page 22 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Jawaharlal Nehru Port - Yantian 40ft / 40ft HC $428 $441 $398 $381 -14% -4% -14%
Jawaharlal Nehru Port - Jebel Ali 20ft $585 $551 $547 $530 -4% -3% -21%
Jawaharlal Nehru Port - Jebel Ali 40ft / 40ft HC $756 $722 $707 $715 -1% 1% -23%
Jawaharlal Nehru Port - Felixstowe 20ft $1,894 $1,616 $1,626 $1,824 13% 12% -50%
Jawaharlal Nehru Port - Felixstowe 40ft / 40ft HC $2,060 $1,808 $2,020 $2,124 17% 5% -44%
Jawaharlal Nehru Port - New York 20ft $2,291 $2,824 $3,122 $3,640 29% 17% 75%
Jawaharlal Nehru Port - New York 40ft / 40ft HC $2,767 $3,147 $3,601 $4,106 30% 14% 61%
Jawaharlal Nehru Port - Houston 20ft $3,209 $3,490 $3,402 $3,803 9% 12% -22%
Jawaharlal Nehru Port - Houston 40ft / 40ft HC $3,841 $4,122 $4,031 $4,368 6% 8% -24%
Jawaharlal Nehru Port - Chicago via Norfolk 20ft $2,964 $3,115 $3,394 $3,947 27% 16% 73%
Jawaharlal Nehru Port - Chicago via Norfolk 40ft / 40ft HC $3,454 $3,578 $3,952 $4,463 25% 13% 56%
Jawaharlal Nehru Port - Memphis via Savannah 20ft $3,126 $2,952 $3,036 $4,005 36% 32% 93%
Jawaharlal Nehru Port - Memphis via Savannah 40ft / 40ft HC $3,732 $3,419 $3,558 $4,779 40% 34% 90%
Jawaharlal Nehru Port - Los Angeles 20ft $3,070 $2,538 $2,756 $3,048 20% 11% -23%
Jawaharlal Nehru Port - Los Angeles 40ft / 40ft HC $3,667 $3,038 $3,255 $3,600 18% 11% -24%
Jawaharlal Nehru Port - Genoa 20ft $2,377 $2,088 $1,878 $1,616 -23% -14% -57%
Jawaharlal Nehru Port - Genoa 40ft / 40ft HC $2,502 $2,180 $1,974 $1,648 -24% -17% -58%
Ashdod - Shanghai 20ft $1,085 $1,399 $854 $1,275 -9% 49% -18%
Ashdod - Shanghai 40ft / 40ft HC $1,250 $1,844 $1,197 $1,820 -1% 52% -10%
Ashdod - Jawaharlal Nehru Port 20ft $1,358 $1,412 $1,368 $1,497 6% 9% -13%
Ashdod - Jawaharlal Nehru Port 40ft / 40ft HC $1,782 $1,807 $1,673 $1,981 10% 18% -23%
Ashdod - Rotterdam 20ft $1,236 $1,543 $1,546 $1,834 19% 19% 35%
Ashdod - Rotterdam 40ft / 40ft HC $1,718 $2,037 $2,051 $2,287 12% 12% 8%
Ashdod - New York 20ft $4,150 $3,635 $3,534 $4,386 21% 24% 27%
Ashdod - New York 40ft / 40ft HC $4,711 $4,614 $4,445 $5,405 17% 22% 28%
Ashdod - Los Angeles 20ft $5,321 $5,378 $5,389 $5,795 8% 8% 1%
Ashdod - Los Angeles 40ft / 40ft HC $6,649 $6,714 $6,668 $6,949 4% 4% -11%
Ashdod - Genoa 20ft $1,338 $1,274 $1,274 $1,342 5% 5% -1%
Ashdod - Genoa 40ft / 40ft HC $1,770 $1,601 $1,601 $1,737 8% 8% 2%
Yokohama - Jawaharlal Nehru Port 20ft $2,182 $1,986 $1,891 $2,338 18% 24% -24%
Yokohama - Jawaharlal Nehru Port 40ft / 40ft HC $3,080 $2,915 $2,658 $3,068 5% 15% -33%
Busan - Jawaharlal Nehru Port 20ft $1,648 $1,468 $1,410 $2,130 45% 51% -9%
Busan - Jawaharlal Nehru Port 40ft / 40ft HC $1,974 $1,710 $1,664 $2,466 44% 48% -20%
Tianjin - Jawaharlal Nehru Port 20ft $1,376 $1,394 $1,072 $2,043 47% 91% -48%
Tianjin - Jawaharlal Nehru Port 40ft / 40ft HC $1,538 $1,531 $1,213 $2,320 52% 91% -47%
Rotterdam - Jawaharlal Nehru Port 20ft $1,186 $1,315 $1,137 $1,059 -19% -7% -30%
Rotterdam - Jawaharlal Nehru Port 40ft / 40ft HC $1,448 $1,491 $1,348 $1,207 -19% -10% -35%
Rotterdam - Dammam 20ft $1,550 $1,412 $1,217 $1,388 -2% 14% -29%
Rotterdam - Dammam 40ft / 40ft HC $1,995 $1,709 $1,478 $1,686 -1% 14% -30%
Rotterdam - Jeddah 20ft $2,097 $1,932 $1,628 $1,432 -26% -12% -44%
Rotterdam - Jeddah 40ft / 40ft HC $2,557 $2,237 $1,978 $1,801 -19% -9% -44%
Rotterdam - Jebel Ali 20ft $1,309 $1,386 $1,440 $1,360 -2% -6% -33%
Rotterdam - Jebel Ali 40ft / 40ft HC $1,883 $1,990 $1,857 $1,672 -16% -10% -32%
Dammam - Shanghai 20ft $453 $454 $458 $478 5% 4% -18%
Dammam - Shanghai 40ft / 40ft HC $603 $639 $649 $694 9% 7% -17%
Dammam - Jawaharlal Nehru Port 20ft $345 $432 $336 $327 -24% -3% -35%
Dammam - Jawaharlal Nehru Port 40ft / 40ft HC $458 $596 $497 $500 -16% 1% -31%
Dammam - Busan 20ft $466 $460 $456 $538 17% 18% -1%
Dammam - Busan 40ft / 40ft HC $742 $729 $716 $836 15% 17% 11%
Dammam - Tianjin 20ft $614 $638 $604 $631 -1% 4% -1%
Dammam - Tianjin 40ft / 40ft HC $777 $812 $809 $869 7% 7% 2%
Dammam - Yantian 20ft $606 $629 $646 $606 -4% -6% 5%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 22 June 2025


=== Page 23 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Dammam - Yantian 40ft / 40ft HC $781 $866 $913 $873 1% -4% 9%
Jeddah - Halifax 20ft $2,477 $2,477 $2,477 $2,711 9% 9% 1%
Jeddah - Halifax 40ft / 40ft HC $3,091 $3,134 $3,134 $3,355 7% 7% 18%
Jeddah - Montreal 20ft $2,524 $2,445 $2,445 $2,600 6% 6% 13%
Jeddah - Montreal 40ft / 40ft HC $3,267 $2,941 $2,941 $3,143 7% 7% 8%
Jeddah - Vancouver 20ft $2,543 $3,412 $3,078 $3,453 1% 12% 11%
Jeddah - Vancouver 40ft / 40ft HC $3,200 $4,254 $3,924 $4,316 1% 10% 25%
Jeddah - Rotterdam 20ft $1,336 $1,164 $1,359 $1,498 29% 10% -13%
Jeddah - Rotterdam 40ft / 40ft HC $1,392 $1,194 $1,456 $1,463 23% 0% -36%
Jeddah - Genoa 20ft $1,023 $1,024 $931 $1,018 -1% 9% -48%
Jeddah - Genoa 40ft / 40ft HC $1,280 $1,281 $1,241 $1,428 11% 15% -42%
Singapore - Jawaharlal Nehru Port 20ft $1,250 $1,193 $1,197 $1,506 26% 26% -41%
Singapore - Jawaharlal Nehru Port 40ft / 40ft HC $1,643 $1,473 $1,520 $2,110 43% 39% -41%
Yantian - Jawaharlal Nehru Port 20ft $1,230 $1,068 $958 $1,479 38% 54% -55%
Yantian - Jawaharlal Nehru Port 40ft / 40ft HC $1,384 $1,132 $1,130 $1,790 58% 58% -51%
Jebel Ali - Toronto via Montreal 20ft $3,632 $3,740 $4,006 $3,932 5% -2% -15%
Jebel Ali - Toronto via Montreal 40ft / 40ft HC $3,934 $4,466 $4,666 $4,608 3% -1% -11%
Jebel Ali - Halifax 20ft $2,697 $2,627 $3,118 $3,010 15% -3% -14%
Jebel Ali - Halifax 40ft / 40ft HC $3,196 $3,096 $3,665 $3,443 11% -6% -17%
Jebel Ali - Montreal 20ft $3,435 $3,620 $3,939 $3,861 7% -2% -15%
Jebel Ali - Montreal 40ft / 40ft HC $3,896 $4,224 $4,575 $4,508 7% -1% -16%
Jebel Ali - Vancouver 20ft $4,391 $3,023 $2,964 $3,618 20% 22% -15%
Jebel Ali - Vancouver 40ft / 40ft HC $4,987 $3,996 $3,634 $4,120 3% 13% -13%
Jebel Ali - Shanghai 20ft $422 $414 $416 $423 2% 2% 1%
Jebel Ali - Shanghai 40ft / 40ft HC $594 $583 $584 $596 2% 2% -1%
Jebel Ali - Jawaharlal Nehru Port 20ft $332 $323 $328 $336 4% 2% -7%
Jebel Ali - Jawaharlal Nehru Port 40ft / 40ft HC $495 $477 $483 $488 2% 1% -6%
Jebel Ali - Yokohama 20ft $629 $684 $865 $902 32% 4% 36%
Jebel Ali - Yokohama 40ft / 40ft HC $884 $936 $1,105 $1,199 28% 9% 14%
Jebel Ali - Busan 20ft $370 $370 $384 $497 34% 29% 15%
Jebel Ali - Busan 40ft / 40ft HC $544 $538 $548 $731 36% 33% 12%
Jebel Ali - Tianjin 20ft $614 $624 $597 $551 -12% -8% 8%
Jebel Ali - Tianjin 40ft / 40ft HC $868 $907 $887 $839 -7% -5% 14%
Jebel Ali - Rotterdam 20ft $2,604 $2,256 $2,217 $2,330 3% 5% -29%
Jebel Ali - Rotterdam 40ft / 40ft HC $2,990 $2,742 $2,550 $2,726 -1% 7% -17%
Jebel Ali - Singapore 20ft $411 $401 $400 $401 0% 0% 3%
Jebel Ali - Singapore 40ft / 40ft HC $586 $576 $572 $578 0% 1% 3%
Jebel Ali - Yantian 20ft $491 $618 $657 $582 -6% -11% 10%
Jebel Ali - Yantian 40ft / 40ft HC $706 $839 $867 $790 -6% -9% 5%
Jebel Ali - Felixstowe 20ft $2,324 $2,132 $2,172 $2,510 18% 16% -25%
Jebel Ali - Felixstowe 40ft / 40ft HC $2,748 $2,500 $2,536 $3,024 21% 19% -22%
Jebel Ali - New York 20ft $3,291 $3,124 $2,957 $2,907 -7% -2% 3%
Jebel Ali - New York 40ft / 40ft HC $3,719 $3,586 $3,486 $3,572 -0% 2% -4%
Jebel Ali - Houston 20ft $3,139 $3,073 $2,573 $3,344 9% 30% 28%
Jebel Ali - Houston 40ft / 40ft HC $3,743 $3,620 $3,110 $3,996 10% 28% 21%
Jebel Ali - Chicago via Norfolk 20ft $3,300 $3,038 $2,865 $3,757 24% 31% 3%
Jebel Ali - Chicago via Norfolk 40ft / 40ft HC $3,915 $3,930 $3,502 $4,610 17% 32% 11%
Jebel Ali - Memphis via Savannah 20ft $3,126 $2,975 $3,183 $4,186 41% 32% 20%
Jebel Ali - Memphis via Savannah 40ft / 40ft HC $3,968 $3,711 $3,663 $4,829 30% 32% 34%
Jebel Ali - Los Angeles 20ft $3,278 $2,961 $2,894 $3,774 27% 30% 5%
Jebel Ali - Los Angeles 40ft / 40ft HC $3,810 $3,497 $3,287 $4,182 20% 27% -6%
Jebel Ali - Genoa 20ft $2,378 $2,280 $2,259 $2,258 -1% -0% -46%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 23 June 2025


=== Page 24 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Jebel Ali - Genoa 40ft / 40ft HC $2,594 $2,600 $2,593 $2,542 -2% -2% -38%
Felixstowe - Jawaharlal Nehru Port 20ft $1,292 $1,393 $1,112 $1,304 -6% 17% -7%
Felixstowe - Jawaharlal Nehru Port 40ft / 40ft HC $1,816 $1,932 $1,608 $1,656 -14% 3% -15%
Felixstowe - Ashdod 20ft $1,751 $1,867 $1,735 $1,967 5% 13% 18%
Felixstowe - Ashdod 40ft / 40ft HC $2,331 $2,412 $2,236 $2,482 3% 11% 4%
Felixstowe - Jeddah 20ft $1,667 $1,867 $1,842 $1,662 -11% -10% -14%
Felixstowe - Jeddah 40ft / 40ft HC $2,267 $2,305 $2,255 $2,134 -7% -5% -24%
Felixstowe - Jebel Ali 20ft $1,262 $1,547 $1,581 $1,584 2% 0% -5%
Felixstowe - Jebel Ali 40ft / 40ft HC $1,403 $1,578 $1,612 $1,709 8% 6% -24%
New York - Jawaharlal Nehru Port 20ft $1,210 $1,518 $1,335 $1,334 -12% -0% 43%
New York - Jawaharlal Nehru Port 40ft / 40ft HC $1,714 $2,078 $1,777 $1,750 -16% -2% 30%
New York - Dammam 20ft $2,746 $2,944 $2,874 $2,728 -7% -5% 49%
New York - Dammam 40ft / 40ft HC $4,260 $4,344 $4,151 $3,939 -9% -5% 65%
New York - Jeddah 20ft $2,451 $2,717 $2,637 $2,804 3% 6% 93%
New York - Jeddah 40ft / 40ft HC $3,225 $3,499 $3,383 $3,558 2% 5% 102%
New York - Jebel Ali 20ft $2,297 $2,435 $2,430 $2,205 -9% -9% 22%
New York - Jebel Ali 40ft / 40ft HC $3,499 $3,681 $3,613 $2,918 -21% -19% 24%
Houston - Jawaharlal Nehru Port 20ft $1,984 $1,871 $1,852 $2,189 17% 18% 23%
Houston - Jawaharlal Nehru Port 40ft / 40ft HC $2,824 $2,658 $2,570 $3,217 21% 25% 26%
Houston - Jeddah 20ft $3,071 $3,151 $3,216 $3,358 7% 4% 14%
Houston - Jeddah 40ft / 40ft HC $4,097 $4,207 $4,218 $4,368 4% 4% 22%
Houston - Jebel Ali 20ft $2,247 $2,334 $2,456 $2,469 6% 1% 42%
Houston - Jebel Ali 40ft / 40ft HC $3,119 $3,173 $3,234 $3,230 2% -0% 33%
Chicago via Norfolk - Jawaharlal Nehru Port 20ft $1,462 $1,490 $1,591 $1,724 16% 8% 114%
Chicago via Norfolk - Jawaharlal Nehru Port 40ft / 40ft HC $1,883 $1,883 $1,986 $2,102 12% 6% 91%
Chicago via Norfolk - Jebel Ali 20ft $2,164 $2,192 $2,421 $1,706 -22% -30% 24%
Chicago via Norfolk - Jebel Ali 40ft / 40ft HC $2,991 $3,160 $3,248 $2,215 -30% -32% 16%
Memphis via Savannah - Jawaharlal Nehru Port 20ft $1,690 $1,725 $1,726 $1,940 12% 12% 89%
Memphis via Savannah - Jawaharlal Nehru Port 40ft / 40ft HC $2,138 $2,137 $2,151 $2,282 7% 6% 56%
Memphis via Savannah - Jebel Ali 20ft $2,513 $2,496 $2,496 $2,041 -18% -18% 10%
Memphis via Savannah - Jebel Ali 40ft / 40ft HC $3,394 $3,332 $3,332 $2,628 -21% -21% 22%
Los Angeles - Jawaharlal Nehru Port 20ft $2,036 $2,031 $2,046 $2,356 16% 15% 33%
Los Angeles - Jawaharlal Nehru Port 40ft / 40ft HC $2,683 $2,683 $2,678 $2,994 12% 12% 41%
Los Angeles - Jeddah 20ft $3,282 $3,473 $3,396 $3,538 2% 4% 24%
Los Angeles - Jeddah 40ft / 40ft HC $4,456 $4,810 $4,529 $4,679 -3% 3% 28%
Los Angeles - Jebel Ali 20ft $2,466 $2,553 $2,674 $2,680 5% 0% 60%
Los Angeles - Jebel Ali 40ft / 40ft HC $3,229 $3,283 $3,344 $3,233 -2% -3% 53%
Genoa - Jawaharlal Nehru Port 20ft $1,123 $1,071 $1,096 $1,091 2% -0% -13%
Genoa - Jawaharlal Nehru Port 40ft / 40ft HC $1,445 $1,331 $1,330 $1,319 -1% -1% -20%
Genoa - Jeddah 20ft $1,009 $1,034 $1,113 $988 -4% -11% -35%
Genoa - Jeddah 40ft / 40ft HC $1,368 $1,223 $1,325 $1,261 3% -5% -40%
Genoa - Jebel Ali 20ft $1,100 $1,075 $1,114 $1,100 2% -1% -12%
Genoa - Jebel Ali 40ft / 40ft HC $1,422 $1,382 $1,434 $1,444 4% 1% -15%
Jawaharlal Nehru Port - Montreal 20ft $3,888 $3,428 $3,428 $3,702 8% 8% -19%
Jawaharlal Nehru Port - Montreal 40ft / 40ft HC $4,444 $3,776 $3,776 $4,256 13% 13% -19%
Dammam - Yokohama 20ft $864 $771 $862 $927 20% 8% -8%
Dammam - Yokohama 40ft / 40ft HC $1,198 $979 $987 $1,138 16% 15% -20%
Antwerp - Visakhapatnam 20ft $1,063 $1,211 $1,344 $1,997 65% 49% 39%
Antwerp - Visakhapatnam 40ft / 40ft HC $1,241 $1,460 $1,880 $2,754 89% 46% 35%
Shanghai - Visakhapatnam 20ft $1,223 $1,080 $1,092 $1,658 54% 52% -53%
Shanghai - Visakhapatnam 40ft / 40ft HC $1,414 $1,181 $1,361 $1,892 60% 39% -54%
Dalian - Visakhapatnam 20ft $1,209 $1,050 $1,139 $1,843 76% 62% -51%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 24 June 2025


=== Page 25 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Dalian - Visakhapatnam 40ft / 40ft HC $1,437 $1,191 $1,482 $2,156 81% 45% -49%
Huangpu - Visakhapatnam 20ft $1,048 $1,067 $1,137 $1,767 66% 55% -40%
Huangpu - Visakhapatnam 40ft / 40ft HC $1,186 $1,256 $1,476 $2,047 63% 39% -43%
Visakhapatnam - Shanghai 20ft $253 $253 $258 $226 -11% -12% -30%
Visakhapatnam - Shanghai 40ft / 40ft HC $366 $351 $347 $322 -8% -7% -25%
Visakhapatnam - Zhangjiagang 20ft $324 $421 $426 $374 -11% -12% -19%
Visakhapatnam - Zhangjiagang 40ft / 40ft HC $480 $625 $631 $550 -12% -13% -2%
Visakhapatnam - Venice 20ft $3,160 $2,924 $2,690 $2,422 -17% -10% -35%
Visakhapatnam - Venice 40ft / 40ft HC $3,768 $3,519 $3,332 $3,012 -14% -10% -31%
Visakhapatnam - Tokuyama-kudamatsu 20ft $853 $858 $876 $890 4% 2% -27%
Visakhapatnam - Tokuyama-kudamatsu 40ft / 40ft HC $1,192 $1,192 $1,214 $1,216 2% 0% -29%
Visakhapatnam - Busan 20ft $238 $256 $188 $277 8% 47% 13%
Visakhapatnam - Busan 40ft / 40ft HC $330 $385 $233 $363 -6% 56% 4%
Visakhapatnam - Sohar 20ft $1,150 $966 $942 $1,110 15% 18% -5%
Visakhapatnam - Sohar 40ft / 40ft HC $1,794 $1,294 $1,236 $1,778 37% 44% 17%
Visakhapatnam - Valencia 20ft $2,343 $1,826 $1,881 $2,580 41% 37% -25%
Visakhapatnam - Valencia 40ft / 40ft HC $2,946 $2,306 $2,498 $3,003 30% 20% -20%
Visakhapatnam - Colombo 20ft $572 $648 $675 $808 25% 20% 2%
Visakhapatnam - Colombo 40ft / 40ft HC $764 $774 $856 $1,024 32% 20% 1%
Visakhapatnam - Kaohsiung 20ft $504 $459 $472 $575 25% 22% 24%
Visakhapatnam - Kaohsiung 40ft / 40ft HC $729 $609 $635 $744 22% 17% 18%
Visakhapatnam - Laem Chabang 20ft $449 $349 $412 $465 33% 13% 11%
Visakhapatnam - Laem Chabang 40ft / 40ft HC $766 $536 $540 $643 20% 19% 10%
Visakhapatnam - Baltimore 20ft $2,550 $2,650 $3,167 $4,874 84% 54% 31%
Visakhapatnam - Baltimore 40ft / 40ft HC $2,988 $3,468 $3,722 $5,296 53% 42% 10%
Kobe - Visakhapatnam 20ft $2,058 $2,033 $1,869 $2,627 29% 41% -14%
Kobe - Visakhapatnam 40ft / 40ft HC $2,760 $2,740 $2,451 $3,243 18% 32% -14%
Gemlik - Visakhapatnam 20ft $1,155 $1,358 $1,740 $2,170 60% 25% -34%
Gemlik - Visakhapatnam 40ft / 40ft HC $1,190 $1,514 $2,086 $2,426 60% 16% -43%
Chittagong - Shanghai 20ft $235 $247 $223 $284 15% 27% 20%
Chittagong - Shanghai 40ft / 40ft HC $376 $410 $353 $456 11% 29% 15%
Chittagong - Los Angeles 20ft $4,025 $3,632 $3,740 $4,263 17% 14% 51%
Chittagong - Los Angeles 40ft / 40ft HC $5,098 $4,529 $4,773 $5,358 18% 12% 55%
Chittagong - Genoa 20ft $3,403 $3,022 $2,894 $3,431 14% 19% -13%
Chittagong - Genoa 40ft / 40ft HC $4,610 $4,031 $3,926 $4,522 12% 15% -7%
Sihanoukville - Rotterdam 20ft $2,576 $1,886 $1,974 $2,234 18% 13% -44%
Sihanoukville - Rotterdam 40ft / 40ft HC $4,278 $2,954 $3,070 $3,468 17% 13% -48%
Montreal - Dammam 20ft $2,523 $2,905 $2,783 $2,515 -13% -10% 3%
Montreal - Dammam 40ft / 40ft HC $3,807 $4,021 $3,891 $3,701 -8% -5% 15%
Shanghai - Chittagong 20ft $1,418 $1,653 $1,605 $1,440 -13% -10% -56%
Shanghai - Chittagong 40ft / 40ft HC $2,085 $2,531 $2,148 $1,982 -22% -8% -52%
Shanghai - Chennai 20ft $1,213 $1,134 $914 $1,599 41% 75% -51%
Shanghai - Chennai 40ft / 40ft HC $1,383 $1,286 $1,100 $1,718 34% 56% -53%
Shanghai - Jeddah 20ft $2,109 $2,515 $2,392 $3,184 27% 33% -29%
Shanghai - Jeddah 40ft / 40ft HC $2,506 $2,911 $2,778 $4,151 43% 49% -24%
Chennai - Shanghai 20ft $214 $214 $253 $269 26% 6% 33%
Chennai - Shanghai 40ft / 40ft HC $308 $317 $378 $407 28% 8% 40%
Chennai - Rotterdam 20ft $3,174 $1,970 $1,982 $1,902 -3% -4% -42%
Chennai - Rotterdam 40ft / 40ft HC $4,371 $2,368 $2,347 $2,219 -6% -5% -43%
Chennai - New York 20ft $3,114 $3,000 $3,246 $4,106 37% 26% 39%
Chennai - New York 40ft / 40ft HC $3,676 $3,459 $3,756 $4,730 37% 26% 23%
Chennai - Houston 20ft $4,882 $4,847 $4,055 $5,023 4% 24% 7%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 25 June 2025


=== Page 26 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Chennai - Houston 40ft / 40ft HC $5,353 $5,700 $4,922 $5,765 1% 17% 7%
Chennai - Los Angeles 20ft $3,903 $3,041 $3,389 $4,331 42% 28% 36%
Chennai - Los Angeles 40ft / 40ft HC $4,705 $3,776 $4,139 $5,288 40% 28% 36%
Chennai - Genoa 20ft $2,659 $2,475 $2,394 $2,356 -5% -2% -15%
Chennai - Genoa 40ft / 40ft HC $3,152 $2,487 $2,419 $2,352 -5% -3% -27%
Jawaharlal Nehru Port - Jeddah 20ft $1,318 $1,344 $1,498 $1,331 -1% -11% -16%
Jawaharlal Nehru Port - Jeddah 40ft / 40ft HC $1,941 $1,848 $2,055 $1,622 -12% -21% -26%
Jawaharlal Nehru Port - Ho Chi Minh City 20ft $252 $256 $256 $254 -1% -1% -25%
Jawaharlal Nehru Port - Ho Chi Minh City 40ft / 40ft HC $384 $395 $395 $393 -1% -1% -15%
Yokohama - Jeddah 20ft $2,711 $2,888 $2,795 $2,956 2% 6% -21%
Yokohama - Jeddah 40ft / 40ft HC $3,991 $4,049 $3,932 $4,127 2% 5% -23%
Busan - Jeddah 20ft $2,625 $2,799 $2,820 $3,099 11% 10% -15%
Busan - Jeddah 40ft / 40ft HC $3,492 $3,653 $3,668 $4,098 12% 12% -12%
Tianjin - Jeddah 20ft $2,258 $2,798 $2,599 $3,175 13% 22% -31%
Tianjin - Jeddah 40ft / 40ft HC $2,768 $3,614 $2,833 $4,225 17% 49% -24%
Rotterdam - Chennai 20ft $1,257 $1,220 $1,169 $1,116 -9% -5% -24%
Rotterdam - Chennai 40ft / 40ft HC $1,570 $1,336 $1,362 $1,295 -3% -5% -31%
Jeddah - New York 20ft $3,114 $2,947 $3,001 $3,421 16% 14% 34%
Jeddah - New York 40ft / 40ft HC $3,921 $3,305 $3,378 $3,995 21% 18% 33%
Singapore - Dammam 20ft $1,432 $1,635 $1,788 $1,902 16% 6% -29%
Singapore - Dammam 40ft / 40ft HC $1,852 $2,023 $2,295 $2,439 21% 6% -29%
Singapore - Jeddah 20ft $2,389 $2,657 $2,805 $3,309 25% 18% -21%
Singapore - Jeddah 40ft / 40ft HC $3,220 $3,387 $3,535 $3,958 17% 12% -34%
Yantian - Jeddah 20ft $3,229 $3,110 $2,818 $3,230 4% 15% -28%
Yantian - Jeddah 40ft / 40ft HC $4,321 $3,943 $3,443 $4,186 6% 22% -27%
Jebel Ali - Ho Chi Minh City 20ft $614 $730 $729 $621 -15% -15% 5%
Jebel Ali - Ho Chi Minh City 40ft / 40ft HC $940 $1,122 $1,106 $848 -24% -23% -10%
New York - Chennai 20ft $2,028 $2,274 $2,274 $2,401 6% 6% 47%
New York - Chennai 40ft / 40ft HC $2,628 $2,964 $2,964 $2,986 1% 1% 38%
Houston - Chennai 20ft $2,236 $2,511 $2,657 $2,681 7% 1% 77%
Houston - Chennai 40ft / 40ft HC $3,071 $3,633 $3,765 $3,698 2% -2% 101%
Los Angeles - Chennai 20ft $2,117 $2,281 $2,259 $2,466 8% 9% 45%
Los Angeles - Chennai 40ft / 40ft HC $2,862 $3,088 $3,060 $3,273 6% 7% 63%
Ho Chi Minh City - Jawaharlal Nehru Port 20ft $1,432 $1,524 $1,372 $1,747 15% 27% -20%
Ho Chi Minh City - Jawaharlal Nehru Port 40ft / 40ft HC $1,832 $1,848 $1,720 $2,181 18% 27% -23%
Ho Chi Minh City - Jebel Ali 20ft $1,419 $1,453 $1,442 $1,559 7% 8% -35%
Ho Chi Minh City - Jebel Ali 40ft / 40ft HC $1,828 $1,921 $1,926 $2,174 13% 13% -39%
Genoa - Chittagong 20ft $1,526 $1,760 $1,830 $2,024 15% 11% -3%
Genoa - Chittagong 40ft / 40ft HC $1,942 $2,372 $2,671 $2,552 8% -4% 2%
Genoa - Chennai 20ft $1,462 $1,689 $1,675 $1,609 -5% -4% -1%
Genoa - Chennai 40ft / 40ft HC $1,942 $2,164 $2,164 $2,096 -3% -3% -5%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 26 June 2025


=== Page 27 ===

Container Freight Rate | Insight
TRANSATLANTIC WESTBOUND INDEX (US$/40FT)
Transatlantic rates Transatlantic Westbound Index (US$/40ft)
$3,500
rise after 5-month
$3,250
slide
$3,000
Drewry’s Transatlantic Westbound Index increased 2%
$2,750
MoM to $2,464 per 40ft container in June—the first
increase since the beginning of the year. However, we
$2,500
expect rates to remain stable in July.
$2,250
Since January 2025, spot rates on Transpacific and Asia-
E
Tr
u
a
r
n
op
sa
e
t l
r
a
o
n
u
t
t
i
e
c
s
t r
h
a
a
d
v
e
e
l a
b
n
e
e
e n
h a
q
v
u
e
i t
b
e
e e
vo
n
l a
re
ti
l
l
a
e
t i
w
ve
h
l
i
y
le
s t
t
a
h
b
o
l
s
e
e
.
on the
Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
Latest demand figures for 1Q25 highlight a contrast in
Drewry Transatlantic Westbound Index (US$/40ft) Rate
Transatlantic cargo volumes: while the North Europe to
Index History
North America route contracted 1% YoY, traffic from the
Mediterranean to North America grew 4% YoY. Sep-24 $2,569
Oct-24 $3,178 % change Sep 24 - Oct 24 24%
From June 2025, Hapag-Lloyd will revise its Caribbean
Express Service (CES) rotation. Nov-24 $3,255 % change Oct 24 - Nov 24 2%
Dec-24 $3,183 % change Nov 24 - Dec 24 -2%
Caucedo will be replaced by Cartagena in Latin America,
while in Europe, Rotterdam will be removed. Meanwhile, Jan-25 $3,143 % change Dec 24 - Jan 25 -1%
MSC has added an eastbound call at Las Palmas (Canary Feb-25 $2,897 % change Jan 25 - Feb 25 -8%
Islands) to its Med-USEC service.
Mar-25 $2,866 % change Feb 25 - Mar 25 -1%
Apr-25 $2,733 % change Mar 25 - Apr 25 -5%
May-25 $2,421 % change Apr 25 - May 25 -11%
Jun-25 $2,464 % change May 25 - Jun 25 2%
Transatlantic Westbound Index (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Rotterdam - New York 20ft $2,435 $2,293 $1,890 $1,819 -21% -4% -5%
Rotterdam - New York 40ft / 40ft HC $2,700 $2,512 $2,071 $1,990 -21% -4% -13%
Rotterdam - Houston 20ft $2,174 $2,436 $2,299 $2,352 -3% 2% 26%
Rotterdam - Houston 40ft / 40ft HC $2,510 $2,832 $2,672 $2,783 -2% 4% 26%
Rotterdam - Los Angeles 20ft $3,415 $2,647 $3,123 $3,135 18% 0% 11%
Rotterdam - Los Angeles 40ft / 40ft HC $4,021 $3,535 $3,619 $3,815 8% 5% 11%
Felixstowe - New York 20ft $2,697 $2,639 $2,517 $2,842 8% 13% 24%
Felixstowe - New York 40ft / 40ft HC $3,117 $3,084 $2,974 $3,304 7% 11% 19%
Felixstowe - Houston 20ft $2,250 $2,562 $2,524 $2,999 17% 19% 46%
Felixstowe - Houston 40ft / 40ft HC $2,507 $2,896 $2,899 $3,347 16% 15% 44%
Felixstowe - Los Angeles 20ft $3,818 $3,199 $3,049 $3,697 16% 21% 16%
Felixstowe - Los Angeles 40ft / 40ft HC $4,558 $3,871 $3,704 $4,624 19% 25% 14%
Rotterdam - Toronto via Montreal 20ft $3,229 $2,904 $2,981 $2,802 -4% -6% 22%
Rotterdam - Toronto via Montreal 40ft / 40ft HC $4,246 $3,348 $3,394 $2,958 -12% -13% 20%
Rotterdam - Halifax 20ft $2,784 $2,930 $2,832 $2,700 -8% -5% 27%
Rotterdam - Halifax 40ft / 40ft HC $3,272 $3,308 $3,148 $3,016 -9% -4% 13%
Rotterdam - Montreal 20ft $2,838 $2,698 $2,533 $2,743 2% 8% 30%
Rotterdam - Montreal 40ft / 40ft HC $3,704 $3,177 $3,060 $3,218 1% 5% 33%
Rotterdam - Vancouver 20ft $4,009 $3,958 $3,859 $3,962 0% 3% 10%
Rotterdam - Vancouver 40ft / 40ft HC $4,983 $4,916 $4,801 $4,862 -1% 1% 12%
Rotterdam - Chicago via Norfolk 20ft $3,028 $2,795 $2,564 $2,019 -28% -21% -13%
Rotterdam - Chicago via Norfolk 40ft / 40ft HC $3,386 $3,135 $2,981 $2,563 -18% -14% -3%
Rotterdam - Memphis via Savannah 20ft $3,149 $2,619 $2,505 $2,429 -7% -3% 22%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 27 June 2025


=== Page 28 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Rotterdam - Memphis via Savannah 40ft / 40ft HC $3,408 $2,813 $2,713 $2,688 -4% -1% 15%
Gdansk - New York 20ft $3,131 $2,582 $2,503 $2,779 8% 11% 20%
Gdansk - New York 40ft / 40ft HC $3,811 $3,155 $3,098 $3,413 8% 10% 19%
Gothenburg - New York 20ft $3,051 $2,636 $2,589 $2,888 10% 12% 16%
Gothenburg - New York 40ft / 40ft HC $3,664 $3,311 $3,106 $3,655 10% 18% 4%
Istanbul - New York 20ft $3,556 $3,556 $3,618 $3,255 -8% -10% 15%
Istanbul - New York 40ft / 40ft HC $3,727 $3,427 $3,683 $3,330 -3% -10% 13%
Istanbul - Houston 20ft $3,521 $3,706 $3,920 $3,575 -4% -9% 33%
Istanbul - Houston 40ft / 40ft HC $4,145 $4,146 $4,276 $3,965 -4% -7% 37%
Istanbul - Los Angeles 20ft $5,076 $5,074 $4,931 $4,772 -6% -3% 11%
Istanbul - Los Angeles 40ft / 40ft HC $5,980 $5,951 $5,883 $6,278 5% 7% 23%
Felixstowe - Halifax 20ft $2,616 $2,616 $2,254 $2,342 -10% 4% -8%
Felixstowe - Halifax 40ft / 40ft HC $2,944 $2,942 $2,614 $2,672 -9% 2% -3%
Felixstowe - Montreal 20ft $2,366 $2,266 $1,954 $2,042 -10% 5% -6%
Felixstowe - Montreal 40ft / 40ft HC $2,694 $2,592 $2,314 $2,427 -6% 5% 6%
Felixstowe - Vancouver 20ft $3,584 $3,183 $2,965 $3,034 -5% 2% -4%
Felixstowe - Vancouver 40ft / 40ft HC $3,978 $3,576 $3,288 $3,366 -6% 2% -1%
Genoa - Toronto via Montreal 20ft $4,019 $3,694 $3,794 $3,806 3% 0% 14%
Genoa - Toronto via Montreal 40ft / 40ft HC $5,485 $5,113 $5,103 $5,092 -0% -0% 22%
Genoa - Halifax 20ft $3,581 $3,369 $3,402 $3,593 7% 6% 25%
Genoa - Halifax 40ft / 40ft HC $4,788 $4,614 $4,665 $4,822 5% 3% 29%
Genoa - Montreal 20ft $3,670 $3,593 $3,603 $3,748 4% 4% 25%
Genoa - Montreal 40ft / 40ft HC $5,269 $4,942 $4,958 $5,171 5% 4% 36%
Genoa - Vancouver 20ft $4,934 $5,190 $5,183 $5,164 -1% -0% 30%
Genoa - Vancouver 40ft / 40ft HC $6,665 $6,990 $6,972 $6,909 -1% -1% 43%
Genoa - New York 20ft $2,724 $2,671 $2,664 $2,719 2% 2% 28%
Genoa - New York 40ft / 40ft HC $3,919 $3,769 $3,789 $3,834 2% 1% 36%
Genoa - Houston 20ft $2,494 $2,793 $3,169 $2,591 -7% -18% 22%
Genoa - Houston 40ft / 40ft HC $3,703 $3,973 $4,350 $4,039 2% -7% 31%
Genoa - Chicago via Norfolk 20ft $3,433 $2,828 $3,064 $3,021 7% -1% 47%
Genoa - Chicago via Norfolk 40ft / 40ft HC $4,149 $3,265 $3,511 $3,568 9% 2% 45%
Genoa - Memphis via Savannah 20ft $3,992 $3,099 $2,979 $2,966 -4% -0% 29%
Genoa - Memphis via Savannah 40ft / 40ft HC $4,817 $3,877 $3,696 $3,716 -4% 1% 35%
Genoa - Los Angeles 20ft $3,343 $3,557 $3,478 $3,374 -5% -3% 24%
Genoa - Los Angeles 40ft / 40ft HC $4,978 $5,216 $5,050 $5,020 -4% -1% 22%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 28 June 2025


=== Page 29 ===

Container Freight Rate | Insight
TRANSATLANTIC EASTBOUND INDEX (US$/40FT)
Backhaul rates to Transatlantic Eastbound Index (US$/40ft)
$1,300
remain stable
$1,250
Drewry's monthly Transatlantic Eastbound Index decreased
4% to $1,210 per 40ft container in June. Meanwhile, spot
rates on this trade were 11% higher YoY and 5% above the $1,200
pre-pandemic levels of 2019, but we expect them to
remain stable in July. $1,150
Monthly trade volumes on the North America to North
$1,100
Europe route decreased 4% YoY in 1Q25, while utilisation
was below 50% during the same period.
Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
Additionally, freight rates on specific routes have also
increased, in line with the index. Rates on the New York–
Rotterdam route decreased 10% in June to $7,81 per 40ft Drewry Transatlantic Eastbound Index (US$/40ft) Rate
container. Index History
Sep-24 $1,109
Oct-24 $1,130 % change Sep 24 - Oct 24 2%
Nov-24 $1,205 % change Oct 24 - Nov 24 7%
Dec-24 $1,250 % change Nov 24 - Dec 24 4%
Jan-25 $1,249 % change Dec 24 - Jan 25 0%
Feb-25 $1,240 % change Jan 25 - Feb 25 -1%
Mar-25 $1,251 % change Feb 25 - Mar 25 1%
Apr-25 $1,219 % change Mar 25 - Apr 25 -3%
May-25 $1,262 % change Apr 25 - May 25 4%
Jun-25 $1,210 % change May 25 - Jun 25 -4%
Transatlantic Eastbound Index (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
New York - Rotterdam 20ft $621 $680 $733 $624 -8% -15% -8%
New York - Rotterdam 40ft / 40ft HC $830 $782 $869 $781 -0% -10% 5%
New York - Felixstowe 20ft $930 $924 $952 $1,114 21% 17% 6%
New York - Felixstowe 40ft / 40ft HC $1,083 $1,027 $1,008 $1,204 17% 19% 7%
Houston - Rotterdam 20ft $1,282 $1,415 $1,440 $1,345 -5% -7% 20%
Houston - Rotterdam 40ft / 40ft HC $1,732 $1,782 $1,769 $1,627 -9% -8% 24%
Houston - Felixstowe 20ft $1,390 $1,391 $1,474 $1,552 12% 5% 15%
Houston - Felixstowe 40ft / 40ft HC $1,561 $1,562 $1,664 $1,732 11% 4% 13%
Los Angeles - Rotterdam 20ft $2,714 $2,978 $2,786 $2,866 -4% 3% 15%
Los Angeles - Rotterdam 40ft / 40ft HC $3,375 $3,277 $3,170 $3,118 -5% -2% 10%
Los Angeles - Felixstowe 20ft $2,450 $2,465 $2,427 $2,698 9% 11% 21%
Los Angeles - Felixstowe 40ft / 40ft HC $2,771 $2,909 $2,980 $2,995 3% 1% 19%
Toronto via Montreal - Rotterdam 20ft $1,538 $1,465 $1,466 $1,461 -0% -0% 19%
Toronto via Montreal - Rotterdam 40ft / 40ft HC $1,923 $1,923 $1,910 $1,898 -1% -1% 32%
Toronto via Montreal - Genoa 20ft $2,017 $1,838 $1,847 $1,826 -1% -1% 8%
Toronto via Montreal - Genoa 40ft / 40ft HC $2,454 $2,496 $2,527 $2,506 0% -1% 29%
Halifax - Rotterdam 20ft $1,531 $1,419 $1,280 $1,273 -10% -1% -19%
Halifax - Rotterdam 40ft / 40ft HC $1,952 $1,910 $1,691 $1,623 -15% -4% -1%
Halifax - Felixstowe 20ft $1,572 $1,599 $1,388 $1,391 -13% 0% -25%
Halifax - Felixstowe 40ft / 40ft HC $2,040 $2,066 $1,736 $1,650 -20% -5% -29%
Halifax - Genoa 20ft $1,879 $1,907 $1,706 $1,673 -12% -2% -8%
Halifax - Genoa 40ft / 40ft HC $3,052 $3,081 $2,770 $2,726 -12% -2% -7%
Montreal - Rotterdam 20ft $1,447 $1,109 $973 $1,009 -9% 4% -16%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 29 June 2025


=== Page 30 ===

Container Freight Rate | Insight
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Montreal - Rotterdam 40ft / 40ft HC $1,724 $1,375 $1,235 $1,306 -5% 6% -4%
Montreal - Felixstowe 20ft $1,404 $1,408 $1,269 $1,096 -22% -14% -20%
Montreal - Felixstowe 40ft / 40ft HC $1,806 $1,813 $1,669 $1,438 -21% -14% -14%
Montreal - Genoa 20ft $1,559 $1,764 $1,572 $1,755 -1% 12% 18%
Montreal - Genoa 40ft / 40ft HC $2,096 $2,472 $2,290 $2,512 2% 10% 36%
Vancouver - Rotterdam 20ft $2,620 $2,655 $2,773 $2,675 1% -4% 4%
Vancouver - Rotterdam 40ft / 40ft HC $4,197 $4,199 $4,240 $3,250 -23% -23% -10%
Vancouver - Felixstowe 20ft $2,956 $2,974 $2,833 $2,912 -2% 3% -2%
Vancouver - Felixstowe 40ft / 40ft HC $4,265 $4,294 $4,073 $3,495 -19% -14% -6%
Vancouver - Genoa 20ft $2,562 $2,615 $2,415 $2,616 0% 8% 2%
Vancouver - Genoa 40ft / 40ft HC $4,150 $4,200 $3,890 $4,090 -3% 5% 0%
New York - Port Said 20ft $1,665 $1,804 $1,791 $1,794 -1% 0% 23%
New York - Port Said 40ft / 40ft HC $2,283 $2,358 $2,342 $2,392 1% 2% 23%
New York - Istanbul 20ft $1,179 $1,350 $1,487 $1,483 10% -0% 22%
New York - Istanbul 40ft / 40ft HC $1,554 $1,762 $2,268 $1,997 13% -12% 27%
New York - Genoa 20ft $816 $922 $959 $970 5% 1% 3%
New York - Genoa 40ft / 40ft HC $887 $998 $1,077 $1,024 3% -5% 11%
Houston - Port Said 20ft $2,482 $2,357 $2,294 $2,298 -3% 0% -4%
Houston - Port Said 40ft / 40ft HC $3,185 $2,962 $2,919 $2,936 -1% 1% 6%
Houston - Istanbul 20ft $2,394 $2,566 $2,572 $2,407 -6% -6% -6%
Houston - Istanbul 40ft / 40ft HC $3,084 $3,354 $3,365 $3,171 -5% -6% -1%
Houston - Genoa 20ft $1,230 $1,377 $1,380 $1,333 -3% -3% 22%
Houston - Genoa 40ft / 40ft HC $1,379 $1,614 $1,619 $1,564 -3% -3% 53%
Chicago via Norfolk - Rotterdam 20ft $1,012 $1,064 $1,090 $986 -7% -10% 59%
Chicago via Norfolk - Rotterdam 40ft / 40ft HC $1,089 $1,160 $1,182 $1,218 5% 3% 85%
Chicago via Norfolk - Genoa 20ft $1,181 $1,231 $1,238 $1,380 12% 11% 90%
Chicago via Norfolk - Genoa 40ft / 40ft HC $1,281 $1,323 $1,337 $1,521 15% 14% 141%
Memphis via Savannah - Rotterdam 20ft $1,356 $1,390 $1,556 $1,963 41% 26% 109%
Memphis via Savannah - Rotterdam 40ft / 40ft HC $1,498 $1,657 $1,874 $2,318 40% 24% 101%
Memphis via Savannah - Genoa 20ft $1,333 $1,319 $1,328 $1,558 18% 17% 70%
Memphis via Savannah - Genoa 40ft / 40ft HC $1,426 $1,395 $1,414 $1,675 20% 18% 52%
Los Angeles - Port Said 20ft $3,631 $3,767 $3,622 $3,659 -3% 1% 0%
Los Angeles - Port Said 40ft / 40ft HC $5,516 $5,529 $4,674 $4,357 -21% -7% -16%
Los Angeles - Istanbul 20ft $3,612 $3,750 $3,696 $3,794 1% 3% 2%
Los Angeles - Istanbul 40ft / 40ft HC $4,169 $4,839 $4,784 $4,882 1% 2% 9%
Los Angeles - Genoa 20ft $3,369 $3,507 $3,510 $3,449 -2% -2% 11%
Los Angeles - Genoa 40ft / 40ft HC $5,567 $5,750 $5,755 $5,733 -0% -0% 30%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 30 June 2025


=== Page 31 ===

Container Freight Rate | Insight
S CHINA-BRAZIL BENCHMARK (US$/40FT)
Rates to increase in S China-Brazil Benchmark (US$/40ft)
$10,000
July
$7,500
Drewry’s key South China to Brazil Index surged 128% in
June to $4,215 per 40ft container after declining
consistently over the past 10 months, marking a 46% YoY $5,000
plunge. However, they remain 145% above pre-pandemic
levels. $2,500
The recent spike was driven by a rebound in cargo
$0
volumes, leading to vessel space shortages and prompting
c
C
a
h
r
i
r
n
ie
e
r
s
s
e p
to
o rt
r
s
a i
a
s
r
e
e
r
e
a
x
t
p
e
e
s
r
.
ie
C
n
o
c
m
ing
p o
e
u
q
n
u
d
i
i
p
n
m
g
en
th
t
e
s h
i
o
ss
rt
u
a
e
g
,
e s
m
t
a
h
j
a
o
t
r
Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
now exceed supply, intensifying rate pressures as shippers
compete for containers. With demand up 17% YoY in April,
these pressures show no signs of easing. Drewry S China-Brazil Benchmark (US$/40ft) Rate Index
History
Drewry expects the uptrend in rates to continue in July. The
Sep-24 $8,084
rerouting of vessels to support busy China–US trade lanes
is further straining equipment availability and vessel space Oct-24 $7,065 % change Sep 24 - Oct 24 -13%
on other routes. A forwarder within Drewry’s global Nov-24 $6,208 % change Oct 24 - Nov 24 -12%
network noted that elevated rates are likely to persist
Dec-24 $5,788 % change Nov 24 - Dec 24 -7%
through July and August, especially as the peak shipping
season gains momentum. Jan-25 $5,506 % change Dec 24 - Jan 25 -5%
Feb-25 $2,974 % change Jan 25 - Feb 25 -46%
Mar-25 $2,947 % change Feb 25 - Mar 25 -1%
Apr-25 $1,963 % change Mar 25 - Apr 25 -33%
May-25 $1,850 % change Apr 25 - May 25 -6%
Jun-25 $4,215 % change May 25 - Jun 25 128%
S China-Brazil Benchmark (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Yantian - Santos 20ft $2,696 $1,680 $1,606 $3,152 88% 96% -55%
Yantian - Santos 40ft / 40ft HC $2,947 $1,963 $1,850 $4,215 115% 128% -46%
Melbourne - Santos 20ft $5,171 $5,466 $5,272 $4,946 -10% -6% 11%
Melbourne - Santos 40ft / 40ft HC $7,549 $7,776 $7,582 $6,350 -18% -16% 7%
Santos - Melbourne 20ft $3,072 $3,051 $2,975 $2,785 -9% -6% -1%
Santos - Melbourne 40ft / 40ft HC $3,994 $3,971 $4,053 $3,791 -5% -6% -2%
Santos - Halifax 20ft $4,888 $4,879 $4,818 $5,046 3% 5% 112%
Santos - Halifax 40ft / 40ft HC $5,513 $5,546 $4,932 $5,445 -2% 10% 132%
Santos - Montreal 20ft $5,729 $5,728 $4,854 $5,580 -3% 15% 98%
Santos - Montreal 40ft / 40ft HC $6,003 $5,994 $5,942 $6,760 13% 14% 105%
Santos - Vancouver 20ft $5,615 $6,274 $6,131 $5,731 -9% -7% 74%
Santos - Vancouver 40ft / 40ft HC $5,943 $6,703 $6,278 $6,085 -9% -3% 80%
Santos - Shanghai 20ft $1,105 $1,076 $939 $1,006 -7% 7% 3%
Santos - Shanghai 40ft / 40ft HC $1,080 $1,067 $1,008 $1,126 6% 12% -6%
Santos - Hong Kong 20ft $1,315 $1,230 $1,232 $1,314 7% 7% 11%
Santos - Hong Kong 40ft / 40ft HC $1,320 $1,316 $1,240 $1,348 2% 9% 5%
Santos - Jawaharlal Nehru Port 20ft $2,557 $2,390 $2,064 $2,097 -12% 2% -2%
Santos - Jawaharlal Nehru Port 40ft / 40ft HC $3,423 $3,327 $3,003 $3,019 -9% 1% 12%
Santos - Yokohama 20ft $1,353 $1,357 $1,391 $1,122 -17% -19% -28%
Santos - Yokohama 40ft / 40ft HC $1,836 $1,706 $1,707 $1,435 -16% -16% -36%
Santos - Busan 20ft $1,007 $988 $984 $905 -8% -8% -23%
Santos - Busan 40ft / 40ft HC $1,118 $1,080 $1,080 $1,101 2% 2% -18%
Santos - Lagos 20ft $3,094 $3,090 $3,768 $3,270 6% -13% -13%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 31 June 2025


=== Page 32 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Santos - Lagos 40ft / 40ft HC $4,737 $4,632 $5,774 $4,676 1% -19% -4%
Santos - Tianjin 20ft $1,162 $1,175 $1,036 $1,163 -1% 12% 13%
Santos - Tianjin 40ft / 40ft HC $1,255 $1,260 $1,082 $1,154 -8% 7% -12%
Santos - Rotterdam 20ft $1,977 $1,832 $1,806 $1,810 -1% 0% 46%
Santos - Rotterdam 40ft / 40ft HC $1,641 $1,476 $1,426 $1,446 -2% 1% 4%
Santos - Jeddah 20ft $2,280 $2,145 $2,146 $2,146 0% 0% -3%
Santos - Jeddah 40ft / 40ft HC $3,454 $3,257 $3,257 $3,257 0% 0% 6%
Santos - Singapore 20ft $1,074 $1,072 $1,003 $1,167 9% 16% 10%
Santos - Singapore 40ft / 40ft HC $1,222 $1,217 $1,175 $1,370 13% 17% 2%
Santos - Durban 20ft $1,795 $1,875 $1,875 $2,114 13% 13% -11%
Santos - Durban 40ft / 40ft HC $2,285 $2,407 $2,423 $2,839 18% 17% 11%
Santos - Yantian 20ft $1,177 $1,115 $881 $1,020 -9% 16% 4%
Santos - Yantian 40ft / 40ft HC $1,220 $1,100 $948 $994 -10% 5% -17%
Santos - Jebel Ali 20ft $2,214 $2,036 $2,035 $2,069 2% 2% -3%
Santos - Jebel Ali 40ft / 40ft HC $3,418 $3,171 $3,171 $2,945 -7% -7% -3%
Santos - Felixstowe 20ft $1,949 $1,948 $2,082 $2,163 11% 4% 20%
Santos - Felixstowe 40ft / 40ft HC $2,417 $2,413 $2,559 $2,590 7% 1% 14%
Santos - New York 20ft $4,258 $4,215 $4,223 $4,332 3% 3% 113%
Santos - New York 40ft / 40ft HC $4,292 $4,277 $4,273 $4,747 11% 11% 115%
Santos - Houston 20ft $3,963 $3,835 $4,102 $4,652 21% 13% 142%
Santos - Houston 40ft / 40ft HC $4,008 $3,880 $4,147 $4,830 24% 16% 118%
Santos - Los Angeles 20ft $4,527 $4,393 $4,347 $4,955 13% 14% 41%
Santos - Los Angeles 40ft / 40ft HC $4,690 $4,540 $4,453 $5,178 14% 16% 37%
Santos - Genoa 20ft $1,699 $1,614 $1,568 $1,712 6% 9% 25%
Santos - Genoa 40ft / 40ft HC $1,923 $1,819 $1,793 $2,002 10% 12% 37%
Halifax - Santos 20ft $1,972 $1,958 $1,908 $1,990 2% 4% -5%
Halifax - Santos 40ft / 40ft HC $2,492 $2,820 $2,382 $2,548 -10% 7% 0%
Montreal - Santos 20ft $2,017 $2,196 $2,153 $2,437 11% 13% 14%
Montreal - Santos 40ft / 40ft HC $2,344 $2,475 $2,479 $2,783 12% 12% 10%
Vancouver - Santos 20ft $2,568 $2,916 $2,737 $2,723 -7% -1% -3%
Vancouver - Santos 40ft / 40ft HC $3,198 $3,744 $3,434 $3,292 -12% -4% -11%
Shanghai - Santos 20ft $3,458 $1,525 $1,938 $4,649 205% 140% -34%
Shanghai - Santos 40ft / 40ft HC $3,888 $1,721 $2,141 $4,873 183% 128% -37%
Shanghai - San Antonio 20ft $1,964 $1,621 $2,288 $4,798 196% 110% -5%
Shanghai - San Antonio 40ft / 40ft HC $2,755 $2,371 $2,655 $5,215 120% 96% -9%
Shanghai - Cartagena (Colombia) 20ft $2,825 $2,605 $2,659 $7,430 185% 179% 0%
Shanghai - Cartagena (Colombia) 40ft / 40ft HC $3,685 $3,215 $3,268 $7,924 146% 142% -2%
Shanghai - Callao 20ft $1,503 $1,593 $2,260 $4,754 198% 110% -18%
Shanghai - Callao 40ft / 40ft HC $2,904 $2,350 $2,634 $5,178 120% 97% -21%
San Antonio - Shanghai 20ft $701 $584 $677 $750 28% 11% -23%
San Antonio - Shanghai 40ft / 40ft HC $968 $623 $806 $842 35% 4% -28%
San Antonio - Tianjin 20ft $700 $597 $842 $905 52% 7% -11%
San Antonio - Tianjin 40ft / 40ft HC $1,040 $743 $1,028 $1,122 51% 9% -10%
San Antonio - Yantian 20ft $719 $623 $778 $799 28% 3% -20%
San Antonio - Yantian 40ft / 40ft HC $1,089 $799 $1,131 $908 14% -20% -24%
San Antonio - Felixstowe 20ft $2,180 $2,178 $1,842 $2,701 24% 47% 79%
San Antonio - Felixstowe 40ft / 40ft HC $1,952 $1,958 $1,844 $2,826 44% 53% 56%
San Antonio - New York 20ft $3,892 $3,894 $3,894 $4,382 13% 13% 106%
San Antonio - New York 40ft / 40ft HC $3,925 $3,912 $3,925 $4,534 16% 16% 81%
San Antonio - Houston 20ft $3,864 $3,866 $3,869 $4,382 13% 13% 109%
San Antonio - Houston 40ft / 40ft HC $3,908 $3,912 $3,925 $4,534 16% 16% 82%
San Antonio - Los Angeles 20ft $3,031 $3,026 $3,036 $3,513 16% 16% 98%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 32 June 2025


=== Page 33 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
San Antonio - Los Angeles 40ft / 40ft HC $2,965 $2,940 $2,983 $3,559 21% 19% 79%
San Antonio - Genoa 20ft $2,340 $2,004 $1,831 $1,952 -3% 7% 20%
San Antonio - Genoa 40ft / 40ft HC $2,225 $2,076 $2,149 $2,216 7% 3% 20%
Cartagena (Colombia) - Shanghai 20ft $736 $599 $574 $630 5% 10% -38%
Cartagena (Colombia) - Shanghai 40ft / 40ft HC $796 $778 $754 $856 10% 14% -34%
Cartagena (Colombia) - Tianjin 20ft $733 $723 $686 $797 10% 16% -27%
Cartagena (Colombia) - Tianjin 40ft / 40ft HC $855 $926 $866 $1,014 10% 17% -21%
Cartagena (Colombia) - Yantian 20ft $673 $698 $614 $686 -2% 12% -31%
Cartagena (Colombia) - Yantian 40ft / 40ft HC $634 $697 $635 $840 21% 32% -31%
Cartagena (Colombia) - Felixstowe 20ft $1,405 $941 $801 $886 -6% 11% -32%
Cartagena (Colombia) - Felixstowe 40ft / 40ft HC $1,740 $1,309 $1,072 $1,269 -3% 18% -25%
Cartagena (Colombia) - New York 20ft $1,839 $2,166 $1,830 $2,000 -8% 9% 8%
Cartagena (Colombia) - New York 40ft / 40ft HC $2,054 $2,490 $1,999 $2,247 -10% 12% 5%
Cartagena (Colombia) - Genoa 20ft $1,392 $1,442 $1,685 $2,108 46% 25% 50%
Cartagena (Colombia) - Genoa 40ft / 40ft HC $1,580 $1,668 $1,768 $2,337 40% 32% 71%
Hong Kong - Santos 20ft $2,257 $1,590 $1,690 $4,022 153% 138% -52%
Hong Kong - Santos 40ft / 40ft HC $2,543 $1,893 $1,960 $4,626 144% 136% -49%
Jawaharlal Nehru Port - Santos 20ft $2,495 $2,347 $1,936 $1,984 -15% 2% -25%
Jawaharlal Nehru Port - Santos 40ft / 40ft HC $2,589 $2,398 $2,116 $2,104 -12% -1% -29%
Ashdod - Santos 20ft $1,881 $1,958 $1,961 $2,394 22% 22% 21%
Ashdod - Santos 40ft / 40ft HC $2,573 $2,615 $2,621 $3,118 19% 19% 12%
Busan - Santos 20ft $2,283 $1,926 $1,702 $4,575 138% 169% -41%
Busan - Santos 40ft / 40ft HC $2,458 $2,105 $1,885 $4,810 129% 155% -41%
Lagos - Santos 20ft $2,442 $2,424 $2,250 $2,007 -17% -11% -43%
Lagos - Santos 40ft / 40ft HC $3,428 $3,224 $3,030 $2,865 -11% -5% -27%
Tianjin - Santos 20ft $2,828 $1,594 $1,713 $2,916 83% 70% -60%
Tianjin - Santos 40ft / 40ft HC $3,043 $1,826 $1,985 $3,145 72% 58% -61%
Tianjin - San Antonio 20ft $1,999 $1,973 $1,773 $4,816 144% 172% 0%
Tianjin - San Antonio 40ft / 40ft HC $2,805 $2,438 $2,038 $5,298 117% 160% -7%
Tianjin - Cartagena (Colombia) 20ft $2,833 $2,833 $2,867 $7,434 162% 159% -5%
Tianjin - Cartagena (Colombia) 40ft / 40ft HC $3,721 $3,471 $3,354 $8,018 131% 139% -7%
Rotterdam - Santos 20ft $758 $788 $921 $867 10% -6% 9%
Rotterdam - Santos 40ft / 40ft HC $870 $897 $1,000 $977 9% -2% 8%
Rotterdam - Callao 20ft $1,844 $1,885 $2,029 $1,840 -2% -9% 25%
Rotterdam - Callao 40ft / 40ft HC $2,597 $2,638 $2,620 $2,533 -4% -3% 32%
Callao - Shanghai 20ft $462 $524 $581 $654 25% 13% -3%
Callao - Shanghai 40ft / 40ft HC $531 $576 $697 $733 27% 5% -4%
Jeddah - Santos 20ft $3,785 $3,822 $3,863 $4,100 7% 6% 43%
Jeddah - Santos 40ft / 40ft HC $4,441 $4,432 $4,432 $4,651 5% 5% 23%
Singapore - Santos 20ft $2,706 $2,040 $2,225 $2,792 37% 25% -63%
Singapore - Santos 40ft / 40ft HC $3,066 $2,399 $2,569 $3,511 46% 37% -57%
Durban - Santos 20ft $2,398 $2,723 $2,353 $2,224 -18% -5% 10%
Durban - Santos 40ft / 40ft HC $3,411 $3,915 $3,387 $3,079 -21% -9% 16%
Yantian - San Antonio 20ft $1,663 $1,630 $1,524 $4,868 199% 219% 0%
Yantian - San Antonio 40ft / 40ft HC $2,341 $2,275 $2,058 $5,319 134% 158% -4%
Yantian - Cartagena (Colombia) 20ft $2,762 $2,662 $2,712 $7,317 175% 170% -9%
Yantian - Cartagena (Colombia) 40ft / 40ft HC $3,789 $3,522 $3,542 $8,011 127% 126% -8%
Jebel Ali - Santos 20ft $2,455 $2,177 $2,211 $2,176 -0% -2% 16%
Jebel Ali - Santos 40ft / 40ft HC $2,250 $2,191 $2,467 $2,566 17% 4% 4%
Felixstowe - Santos 20ft $738 $774 $531 $774 0% 46% 0%
Felixstowe - Santos 40ft / 40ft HC $946 $979 $590 $907 -7% 54% -9%
Felixstowe - San Antonio 20ft $1,456 $1,556 $1,556 $2,086 34% 34% 22%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 33 June 2025


=== Page 34 ===

Container Freight Rate | Insight
% change
Apr 25May 25 Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Felixstowe - San Antonio 40ft / 40ft HC $1,643 $1,743 $1,743 $2,469 42% 42% 18%
Felixstowe - Cartagena (Colombia) 20ft $1,628 $1,631 $1,597 $1,816 11% 14% 97%
Felixstowe - Cartagena (Colombia) 40ft / 40ft HC $2,381 $2,384 $2,284 $2,620 10% 15% 92%
New York - Santos 20ft $1,091 $1,241 $1,215 $1,050 -15% -14% -9%
New York - Santos 40ft / 40ft HC $1,536 $1,743 $1,574 $1,516 -13% -4% 1%
New York - San Antonio 20ft $1,578 $1,764 $1,847 $1,635 -7% -11% 17%
New York - San Antonio 40ft / 40ft HC $2,025 $2,256 $2,315 $2,030 -10% -12% 18%
New York - Cartagena (Colombia) 20ft $1,212 $1,323 $1,354 $1,510 14% 12% 22%
New York - Cartagena (Colombia) 40ft / 40ft HC $1,329 $1,477 $1,522 $1,626 10% 7% 29%
Houston - Santos 20ft $1,076 $1,216 $1,237 $1,387 14% 12% 37%
Houston - Santos 40ft / 40ft HC $1,426 $1,611 $1,613 $1,736 8% 8% 23%
Houston - San Antonio 20ft $1,974 $2,221 $2,030 $2,067 -7% 2% 20%
Houston - San Antonio 40ft / 40ft HC $2,423 $2,796 $2,407 $2,389 -15% -1% 10%
Houston - Cartagena (Colombia) 20ft $1,150 $1,259 $1,221 $1,367 9% 12% 16%
Houston - Cartagena (Colombia) 40ft / 40ft HC $1,341 $1,479 $1,432 $1,560 5% 9% 12%
Los Angeles - Santos 20ft $2,068 $2,195 $1,968 $2,128 -3% 8% -2%
Los Angeles - Santos 40ft / 40ft HC $2,658 $2,858 $2,505 $2,656 -7% 6% -13%
Los Angeles - San Antonio 20ft $2,261 $2,302 $2,004 $2,097 -9% 5% 12%
Los Angeles - San Antonio 40ft / 40ft HC $2,998 $3,343 $2,743 $2,774 -17% 1% -4%
Los Angeles - Cartagena (Colombia) 20ft $1,624 $1,943 $1,709 $1,809 -7% 6% 9%
Los Angeles - Cartagena (Colombia) 40ft / 40ft HC $2,171 $2,507 $2,083 $2,085 -17% 0% -4%
Genoa - Santos 20ft $919 $1,026 $1,074 $984 -4% -8% 5%
Genoa - Santos 40ft / 40ft HC $1,331 $1,474 $1,531 $1,462 -1% -5% 8%
Genoa - San Antonio 20ft $1,975 $2,218 $2,410 $2,299 4% -5% 20%
Genoa - San Antonio 40ft / 40ft HC $3,166 $3,610 $3,991 $3,609 -0% -10% 28%
Genoa - Cartagena (Colombia) 20ft $1,729 $1,976 $1,983 $2,033 3% 3% 16%
Genoa - Cartagena (Colombia) 40ft / 40ft HC $2,721 $2,991 $2,620 $3,113 4% 19% 22%
Genoa - Callao 20ft - $2,205 $2,400 $2,253 2% -6% -
Genoa - Callao 40ft / 40ft HC - $3,604 $3,988 $3,570 -1% -10% -
Yokohama - Santos 20ft $4,418 $3,003 $2,747 $3,533 18% 29% -55%
Yokohama - Santos 40ft / 40ft HC $5,110 $3,656 $3,420 $4,264 17% 25% -53%
Shanghai - Buenos Aires 20ft $3,293 $2,030 $1,761 $3,782 86% 115% -53%
Shanghai - Buenos Aires 40ft / 40ft HC $3,551 $2,104 $1,907 $4,079 94% 114% -52%
Rotterdam - Buenos Aires 20ft $764 $873 $1,032 $1,027 18% -0% 40%
Rotterdam - Buenos Aires 40ft / 40ft HC $937 $1,013 $1,115 $1,159 14% 4% 21%
New York - Buenos Aires 20ft $1,395 $1,661 $1,661 $1,776 7% 7% 46%
New York - Buenos Aires 40ft / 40ft HC $1,600 $1,751 $1,751 $2,055 17% 17% 61%
New York - Callao 20ft $1,362 $1,767 $1,850 $1,606 -9% -13% 1%
New York - Callao 40ft / 40ft HC $1,723 $2,266 $2,325 $2,008 -11% -14% 11%
Houston - Buenos Aires 20ft $1,135 $1,305 $1,227 $1,416 9% 15% 59%
Houston - Buenos Aires 40ft / 40ft HC $1,447 $1,532 $1,507 $1,734 13% 15% 54%
Los Angeles - Buenos Aires 20ft $1,850 $2,130 $2,178 $2,166 2% -1% 7%
Los Angeles - Buenos Aires 40ft / 40ft HC $2,295 $2,447 $2,459 $2,699 10% 10% 18%
Los Angeles - Callao 20ft $1,392 $2,289 $1,994 $2,067 -10% 4% 8%
Los Angeles - Callao 40ft / 40ft HC $1,893 $3,337 $2,740 $2,751 -18% 0% 23%
Ho Chi Minh City - Santos 20ft $2,820 $1,851 $1,584 $3,755 103% 137% -51%
Ho Chi Minh City - Santos 40ft / 40ft HC $3,154 $2,197 $2,038 $4,157 89% 104% -48%
Genoa - Buenos Aires 20ft $1,103 $1,389 $1,441 $1,332 -4% -8% 39%
Genoa - Buenos Aires 40ft / 40ft HC $1,545 $1,949 $2,017 $1,824 -6% -10% 38%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 34 June 2025


=== Page 35 ===

Container Freight Rate | Insight
S CHINA-SOUTH AFRICA BENCHMARK (US$/40FT)
Rates to remain stable S China-South Africa Benchmark (US$/40ft)
$8,000
Drewry's South China-South Africa Container Rate Index
jumped 30% MoM, reaching $3,278 in June, marking the
first increase in 12 months. However, the current rates are
$6,000
still 62% lower year on year.
This substantial rise can be attributed to a significant
rebound in cargo volumes, particularly as exporters hurry $4,000
to send out goods in anticipation of the peak season. The
latest demand figures from April also show an 8% MoM
increase. This surge in demand has created space $2,000
s
D
h
r
o
e
r
w
ta
ry
g e
e
s
x p
o
e
n
c t
v
s
e
r
s
a
s
t
e
e
ls
s
,
to
p u
s
s
t
h
a
i
b
n
i
g
lis
c
e
a
i
r
n
r i
J
e
u
r
l
s
y .
to raise their rates.
Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
Several major routes experienced significant rate hikes in
June. For instance, rates from Shanghai to Durban rose Drewry S China-South Africa Benchmark (US$/40ft) Rate
35% to $3,164 for a 40-ft container and those from Tianjin Index History
to Durban jumped 40% to $3,601.
Sep-24 $7,015
Oct-24 $6,465 % change Sep 24 - Oct 24 -8%
Nov-24 $5,935 % change Oct 24 - Nov 24 -8%
Dec-24 $4,832 % change Nov 24 - Dec 24 -19%
Jan-25 $4,486 % change Dec 24 - Jan 25 -7%
Feb-25 $4,124 % change Jan 25 - Feb 25 -8%
Mar-25 $3,905 % change Feb 25 - Mar 25 -5%
Apr-25 $3,027 % change Mar 25 - Apr 25 -22%
May-25 $2,516 % change Apr 25 - May 25 -17%
Jun-25 $3,278 % change May 25 - Jun 25 30%
S China-South Africa Benchmark (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Yantian - Durban 20ft $3,145 $2,329 $2,049 $2,530 9% 23% -50%
Yantian - Durban 40ft / 40ft HC $3,905 $3,027 $2,516 $3,278 8% 30% -62%
Halifax - Lagos 20ft $3,187 $3,103 $2,823 $2,801 -10% -1% -26%
Halifax - Lagos 40ft / 40ft HC $5,139 $5,139 $4,706 $4,672 -9% -1% -17%
Halifax - Durban 20ft $3,706 $3,652 $3,457 $3,839 5% 11% 0%
Halifax - Durban 40ft / 40ft HC $5,401 $5,347 $5,016 $5,493 3% 10% -2%
Montreal - Lagos 20ft $3,854 $3,491 $2,998 $3,272 -6% 9% -6%
Montreal - Lagos 40ft / 40ft HC $3,900 $4,483 $4,392 $4,693 5% 7% 21%
Montreal - Durban 20ft $3,501 $3,502 $3,310 $3,692 5% 12% 2%
Montreal - Durban 40ft / 40ft HC $5,049 $5,049 $4,798 $5,275 4% 10% 2%
Vancouver - Lagos 20ft $4,423 $4,023 $3,425 $4,147 3% 21% 12%
Vancouver - Lagos 40ft / 40ft HC $5,447 $5,374 $4,989 $5,230 -3% 5% 7%
Vancouver - Durban 20ft $3,650 $3,753 $3,559 $3,927 5% 10% 13%
Vancouver - Durban 40ft / 40ft HC $5,312 $5,316 $4,988 $5,458 3% 9% 13%
Shanghai - Mombasa 20ft $1,827 $1,814 $2,160 $2,895 60% 34% -24%
Shanghai - Mombasa 40ft / 40ft HC $2,311 $2,227 $2,777 $4,258 91% 53% -25%
Shanghai - Lagos 20ft $3,313 $3,647 $3,592 $4,016 10% 12% -32%
Shanghai - Lagos 40ft / 40ft HC $3,985 $4,685 $4,564 $5,147 10% 13% -43%
Shanghai - Durban 20ft $2,877 $2,452 $2,048 $2,479 1% 21% -51%
Shanghai - Durban 40ft / 40ft HC $3,299 $3,053 $2,346 $3,164 4% 35% -62%
Jawaharlal Nehru Port - Mombasa 20ft $1,664 $1,281 $1,130 $1,125 -12% -0% -28%
Jawaharlal Nehru Port - Mombasa 40ft / 40ft HC $2,058 $1,541 $1,441 $1,426 -7% -1% -31%
Visakhapatnam - Abidjan 20ft $2,654 $2,482 $2,454 $2,847 15% 16% -27%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 35 June 2025


=== Page 36 ===

Container Freight Rate | Insight
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Visakhapatnam - Abidjan 40ft / 40ft HC $4,278 $4,016 $3,878 $4,144 3% 7% -20%
Ashdod - Lagos 20ft $2,569 $2,623 $2,714 $2,684 2% -1% -2%
Ashdod - Lagos 40ft / 40ft HC $3,258 $3,284 $3,340 $3,389 3% 1% -9%
Yokohama - Lagos 20ft $3,699 $3,673 $3,564 $4,346 18% 22% -38%
Yokohama - Lagos 40ft / 40ft HC $5,110 $5,099 $4,902 $6,395 25% 30% -35%
Yokohama - Durban 20ft $3,633 $3,414 $2,787 $3,169 -7% 14% -35%
Yokohama - Durban 40ft / 40ft HC $4,854 $4,346 $3,528 $4,211 -3% 19% -39%
Mombasa - Shanghai 20ft $681 $681 $681 $687 1% 1% 9%
Mombasa - Shanghai 40ft / 40ft HC $1,004 $959 $959 $978 2% 2% 1%
Mombasa - Rotterdam 20ft $2,112 $2,100 $2,111 $2,112 1% 0% 16%
Mombasa - Rotterdam 40ft / 40ft HC $3,134 $3,108 $3,168 $3,118 0% -2% 6%
Mombasa - Genoa 20ft $1,834 $1,834 $1,836 $1,887 3% 3% -46%
Mombasa - Genoa 40ft / 40ft HC $3,031 $2,998 $3,000 $3,033 1% 1% -28%
Busan - Lagos 20ft $3,027 $2,766 $2,683 $3,333 20% 24% -40%
Busan - Lagos 40ft / 40ft HC $4,076 $3,841 $3,697 $4,739 23% 28% -40%
Busan - Durban 20ft $3,568 $3,138 $2,020 $2,862 -9% 42% -35%
Busan - Durban 40ft / 40ft HC $4,297 $3,757 $2,504 $3,910 4% 56% -38%
Lagos - Halifax 20ft $2,780 $2,500 $2,314 $2,583 3% 12% -34%
Lagos - Halifax 40ft / 40ft HC $2,830 $2,793 $2,714 $3,348 20% 23% -36%
Lagos - Montreal 20ft $2,268 $1,782 $1,697 $2,280 28% 34% -42%
Lagos - Montreal 40ft / 40ft HC $3,857 $3,000 $2,850 $3,230 8% 13% -37%
Lagos - Vancouver 20ft $3,158 $2,752 $2,890 $3,499 27% 21% -6%
Lagos - Vancouver 40ft / 40ft HC $4,861 $4,042 $3,702 $4,526 12% 22% -15%
Lagos - Shanghai 20ft $660 $706 $708 $739 5% 4% -13%
Lagos - Shanghai 40ft / 40ft HC $883 $902 $937 $956 6% 2% -5%
Lagos - Yokohama 20ft $780 $731 $660 $632 -14% -4% -48%
Lagos - Yokohama 40ft / 40ft HC $837 $788 $728 $832 6% 14% -41%
Lagos - Busan 20ft $584 $580 $578 $609 5% 5% -28%
Lagos - Busan 40ft / 40ft HC $833 $823 $820 $845 3% 3% -23%
Lagos - Tianjin 20ft $734 $763 $668 $652 -15% -2% -22%
Lagos - Tianjin 40ft / 40ft HC $938 $943 $843 $802 -15% -5% -22%
Lagos - Rotterdam 20ft $1,258 $732 $880 $824 13% -6% -42%
Lagos - Rotterdam 40ft / 40ft HC $1,631 $968 $1,322 $1,127 16% -15% -41%
Lagos - Yantian 20ft $579 $619 $702 $616 -0% -12% -22%
Lagos - Yantian 40ft / 40ft HC $802 $826 $928 $844 2% -9% -8%
Lagos - Genoa 20ft $805 $806 $827 $858 6% 4% -11%
Lagos - Genoa 40ft / 40ft HC $1,036 $1,034 $1,076 $1,136 10% 6% -20%
Tianjin - Lagos 20ft $3,446 $4,130 $3,305 $5,031 22% 52% -15%
Tianjin - Lagos 40ft / 40ft HC $4,189 $4,840 $4,240 $6,501 34% 53% -26%
Tianjin - Durban 20ft $2,759 $2,392 $2,250 $2,817 18% 25% -45%
Tianjin - Durban 40ft / 40ft HC $3,322 $3,112 $2,569 $3,601 16% 40% -59%
Rotterdam - Mombasa 20ft $1,724 $1,961 $1,961 $1,933 -1% -1% -16%
Rotterdam - Mombasa 40ft / 40ft HC $2,556 $3,299 $3,298 $3,269 -1% -1% -16%
Rotterdam - Lagos 20ft $2,106 $2,292 $2,421 $2,431 6% 0% 62%
Rotterdam - Lagos 40ft / 40ft HC $2,773 $2,975 $3,136 $3,146 6% 0% 43%
Rotterdam - Durban 20ft $1,184 $1,028 $1,031 $981 -5% -5% -24%
Rotterdam - Durban 40ft / 40ft HC $1,913 $1,625 $1,607 $1,566 -4% -3% -27%
Durban - Halifax 20ft $3,409 $3,340 $3,408 $3,569 7% 5% -5%
Durban - Halifax 40ft / 40ft HC $6,344 $5,829 $5,814 $6,057 4% 4% -8%
Durban - Montreal 20ft $4,414 $4,268 $4,044 $4,117 -4% 2% -12%
Durban - Montreal 40ft / 40ft HC $7,066 $6,178 $5,893 $6,800 10% 15% -14%
Durban - Vancouver 20ft $4,687 $4,517 $4,747 $4,207 -7% -11% -16%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 36 June 2025


=== Page 37 ===

Container Freight Rate | Insight
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Durban - Vancouver 40ft / 40ft HC $7,672 $6,279 $7,086 $6,839 9% -3% -14%
Durban - Shanghai 20ft $1,009 $1,167 $1,166 $1,079 -8% -7% -5%
Durban - Shanghai 40ft / 40ft HC $1,116 $1,355 $1,389 $1,246 -8% -10% -10%
Durban - Yokohama 20ft $1,269 $1,288 $1,462 $1,441 12% -1% 3%
Durban - Yokohama 40ft / 40ft HC $1,628 $1,639 $1,937 $1,824 11% -6% -8%
Durban - Busan 20ft $1,529 $1,511 $1,658 $1,857 23% 12% 33%
Durban - Busan 40ft / 40ft HC $1,883 $1,861 $2,219 $2,340 26% 5% 45%
Durban - Tianjin 20ft $903 $992 $1,073 $1,096 10% 2% 2%
Durban - Tianjin 40ft / 40ft HC $1,037 $1,243 $1,361 $1,318 6% -3% -4%
Durban - Rotterdam 20ft $2,436 $2,042 $1,880 $1,999 -2% 6% -17%
Durban - Rotterdam 40ft / 40ft HC $2,606 $2,500 $2,122 $2,132 -15% 0% -16%
Durban - Yantian 20ft $984 $1,108 $1,157 $823 -26% -29% -21%
Durban - Yantian 40ft / 40ft HC $1,107 $1,307 $1,397 $915 -30% -35% -31%
Durban - Felixstowe 20ft $2,637 $2,404 $2,627 $2,598 8% -1% -1%
Durban - Felixstowe 40ft / 40ft HC $3,389 $2,801 $3,090 $3,028 8% -2% 4%
Durban - New York 20ft $3,871 $3,735 $4,286 $3,975 6% -7% 2%
Durban - New York 40ft / 40ft HC $6,556 $5,567 $6,661 $6,833 23% 3% 15%
Durban - Houston 20ft $3,938 $3,772 $4,544 $4,180 11% -8% 1%
Durban - Houston 40ft / 40ft HC $6,656 $5,900 $7,086 $7,048 19% -1% 15%
Durban - Los Angeles 20ft $3,701 $3,815 $4,532 $4,506 18% -1% 14%
Durban - Los Angeles 40ft / 40ft HC $5,660 $5,691 $7,098 $6,913 21% -3% 28%
Durban - Genoa 20ft $2,925 $2,922 $2,902 $2,322 -21% -20% -10%
Durban - Genoa 40ft / 40ft HC $3,177 $3,176 $3,196 $2,551 -20% -20% -13%
Yantian - Lagos 20ft $4,103 $4,453 $4,426 $4,786 7% 8% -19%
Yantian - Lagos 40ft / 40ft HC $4,991 $5,395 $5,101 $6,163 14% 21% -34%
Jebel Ali - Mombasa 20ft $2,015 $2,090 $1,761 $1,447 -31% -18% -5%
Jebel Ali - Mombasa 40ft / 40ft HC $2,564 $2,314 $1,983 $1,846 -20% -7% -19%
Felixstowe - Durban 20ft $1,578 $1,550 $1,109 $1,172 -24% 6% -28%
Felixstowe - Durban 40ft / 40ft HC $2,610 $2,556 $1,922 $1,977 -23% 3% -27%
New York - Mombasa 20ft $3,050 $3,234 $3,242 $3,342 3% 3% 28%
New York - Mombasa 40ft / 40ft HC $4,354 $4,648 $4,666 $4,748 2% 2% 17%
New York - Durban 20ft $3,673 $3,850 $3,803 $3,778 -2% -1% 1%
New York - Durban 40ft / 40ft HC $6,071 $6,319 $5,788 $5,908 -7% 2% -7%
Houston - Mombasa 20ft $3,809 $3,852 $3,862 $3,997 4% 3% 33%
Houston - Mombasa 40ft / 40ft HC $5,265 $5,319 $5,343 $5,489 3% 3% 21%
Houston - Durban 20ft $3,941 $4,117 $4,023 $4,107 -0% 2% -7%
Houston - Durban 40ft / 40ft HC $6,396 $6,611 $5,683 $6,400 -3% 13% -8%
Los Angeles - Durban 20ft $4,235 $4,378 $4,390 $4,303 -2% -2% -9%
Los Angeles - Durban 40ft / 40ft HC $7,028 $7,218 $6,987 $6,931 -4% -1% -9%
Genoa - Mombasa 20ft $1,625 $1,608 $1,493 $1,539 -4% 3% -27%
Genoa - Mombasa 40ft / 40ft HC $2,374 $2,357 $2,424 $2,296 -3% -5% -24%
Genoa - Lagos 20ft $1,962 $1,995 $2,144 $2,094 5% -2% 2%
Genoa - Lagos 40ft / 40ft HC $2,700 $2,814 $2,886 $2,966 5% 3% 4%
Genoa - Durban 20ft $1,324 $1,301 $1,329 $1,240 -5% -7% -12%
Genoa - Durban 40ft / 40ft HC $2,338 $2,235 $2,284 $2,243 0% -2% -9%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 37 June 2025


=== Page 38 ===

Container Freight Rate | Insight
S CHINA-AUSTRALIA BENCHMARK (US$/40FT)
Rates to remain stable S China-Australia Benchmark (US$/40ft)
$6,000
in July
$5,000
Drewry's key South China-Australia benchmark declined
4.8% to $2,083 per 40ft container in June. This represents
a contraction of 40% YoY but an increase of 54% compared $4,000
to pre-pandemic levels. We anticipate that rates will
remain stable in July. $3,000
Freight rates have been falling since February as shipping
$2,000
companies struggled to secure enough cargo for their
v
ro
e
u
s
t
s
e
e
s
ls
, al
d
o
e
n
s
g
p i
w
te
it h
v
s
e
e
s
r
s
v
e
ic
l
e
r
c
e
h
d
a
e
n
p
g
lo
e
y
s
m
. T
e
h
n
i
t
s i
t
m
o
pa
h
c
ig
te
h
d
e r
c
-v
a
o
p
l
a
u
c
m
it
e
y Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
and introduced inconsistencies, bringing about blank
sailings and port omissions with route adjustments.
Drewry S China-Australia Benchmark (US$/40ft) Rate Index
Following this trend, rates on the Yantian–Melbourne route History
fell 5% in June, reaching $2,083 per 40ft container.
Sep-24 $4,764
Meanwhile, rates on the Busan-Melbourne route decreased
6%, to $1,924 per 40ft container. Oct-24 $4,246 % change Sep 24 - Oct 24 -11%
Nov-24 $5,112 % change Oct 24 - Nov 24 20%
Dec-24 $4,546 % change Nov 24 - Dec 24 -11%
Jan-25 $4,646 % change Dec 24 - Jan 25 2%
Feb-25 $2,962 % change Jan 25 - Feb 25 -36%
Mar-25 $2,329 % change Feb 25 - Mar 25 -21%
Apr-25 $2,432 % change Mar 25 - Apr 25 4%
May-25 $2,187 % change Apr 25 - May 25 -10%
Jun-25 $2,083 % change May 25 - Jun 25 -5%
S China-Australia Benchmark (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Yantian - Melbourne 20ft $1,516 $1,556 $1,323 $1,161 -25% -12% -38%
Yantian - Melbourne 40ft / 40ft HC $2,329 $2,432 $2,187 $2,083 -14% -5% -40%
Brisbane - Shanghai 20ft $892 $811 $712 $669 -18% -6% -13%
Brisbane - Shanghai 40ft / 40ft HC $1,154 $1,015 $772 $846 -17% 10% -21%
Brisbane - Tianjin 20ft $1,005 $778 $898 $1,043 34% 16% 27%
Brisbane - Tianjin 40ft / 40ft HC $1,328 $963 $1,150 $1,364 42% 19% 20%
Brisbane - Yantian 20ft $888 $810 $726 $805 -1% 11% 2%
Brisbane - Yantian 40ft / 40ft HC $1,155 $991 $941 $929 -6% -1% -14%
Melbourne - Toronto via New York 20ft $4,529 $5,505 $5,182 $4,471 -19% -14% 13%
Melbourne - Toronto via New York 40ft / 40ft HC $6,133 $6,772 $6,177 $6,096 -10% -1% 23%
Melbourne - Halifax 20ft $5,474 $5,477 $4,533 $5,019 -8% 11% 21%
Melbourne - Halifax 40ft / 40ft HC $7,138 $7,140 $6,138 $6,260 -12% 2% 3%
Melbourne - Montreal 20ft $4,535 $4,537 $4,435 $5,082 12% 15% 31%
Melbourne - Montreal 40ft / 40ft HC $5,900 $5,909 $5,793 $6,393 8% 10% 28%
Melbourne - Vancouver 20ft $3,680 $3,882 $3,637 $3,853 -1% 6% 15%
Melbourne - Vancouver 40ft / 40ft HC $4,688 $4,940 $4,646 $4,859 -2% 5% 16%
Melbourne - Shanghai 20ft $793 $786 $687 $667 -15% -3% -15%
Melbourne - Shanghai 40ft / 40ft HC $1,019 $959 $716 $833 -13% 16% -21%
Melbourne - Yokohama 20ft $1,021 $987 $843 $1,042 6% 24% 9%
Melbourne - Yokohama 40ft / 40ft HC $1,318 $1,315 $1,109 $1,256 -4% 13% -10%
Melbourne - Busan 20ft $842 $841 $587 $609 -28% 4% -25%
Melbourne - Busan 40ft / 40ft HC $1,081 $1,078 $731 $736 -32% 1% -34%
Melbourne - Tianjin 20ft $786 $753 $853 $1,041 38% 22% 12%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 38 June 2025


=== Page 39 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Melbourne - Tianjin 40ft / 40ft HC $978 $907 $1,057 $1,351 49% 28% 8%
Melbourne - Rotterdam 20ft $3,349 $3,349 $3,160 $2,913 -13% -8% -34%
Melbourne - Rotterdam 40ft / 40ft HC $4,525 $4,428 $4,429 $3,925 -11% -11% -38%
Melbourne - Singapore 20ft $883 $889 $627 $411 -54% -34% -47%
Melbourne - Singapore 40ft / 40ft HC $1,178 $1,285 $694 $682 -47% -2% -21%
Melbourne - Yantian 20ft $765 $785 $667 $769 -2% 15% -1%
Melbourne - Yantian 40ft / 40ft HC $925 $935 $825 $857 -8% 4% -18%
Melbourne - Felixstowe 20ft $4,019 $3,929 $3,476 $3,096 -21% -11% -2%
Melbourne - Felixstowe 40ft / 40ft HC $5,860 $5,790 $4,788 $4,024 -31% -16% -13%
Melbourne - New York 20ft $4,425 $4,494 $4,604 $4,346 -3% -6% 11%
Melbourne - New York 40ft / 40ft HC $5,780 $6,441 $5,815 $5,596 -13% -4% 4%
Melbourne - Houston 20ft $4,351 $4,153 $4,849 $4,276 3% -12% 19%
Melbourne - Houston 40ft / 40ft HC $6,662 $6,556 $6,541 $5,907 -10% -10% 15%
Melbourne - Chicago via LA-LB 20ft $4,174 $4,028 $3,120 $3,264 -19% 5% -2%
Melbourne - Chicago via LA-LB 40ft / 40ft HC $5,355 $5,130 $3,982 $4,368 -15% 10% 1%
Melbourne - Los Angeles 20ft $2,767 $2,662 $2,774 $2,393 -10% -14% -10%
Melbourne - Los Angeles 40ft / 40ft HC $3,736 $3,515 $3,544 $3,086 -12% -13% -10%
Melbourne - Genoa 20ft $2,877 $2,887 $2,872 $2,808 -3% -2% -43%
Melbourne - Genoa 40ft / 40ft HC $4,143 $4,143 $3,976 $3,848 -7% -3% -44%
Toronto via New York - Melbourne 20ft $2,912 $3,164 $2,797 $2,643 -16% -6% -8%
Toronto via New York - Melbourne 40ft / 40ft HC $4,260 $4,663 $4,079 $3,412 -27% -16% -25%
Halifax - Melbourne 20ft $3,917 $3,311 $3,213 $3,538 7% 10% 2%
Halifax - Melbourne 40ft / 40ft HC $6,768 $5,725 $4,619 $4,577 -20% -1% -20%
Montreal - Melbourne 20ft $3,763 $3,099 $2,536 $2,606 -16% 3% -23%
Montreal - Melbourne 40ft / 40ft HC $4,842 $3,969 $3,342 $3,432 -14% 3% -37%
Vancouver - Melbourne 20ft $2,269 $2,267 $2,126 $2,346 3% 10% -10%
Vancouver - Melbourne 40ft / 40ft HC $3,449 $3,446 $3,227 $3,399 -1% 5% -11%
Shanghai - Brisbane 20ft $1,611 $1,326 $1,163 $1,146 -14% -1% -38%
Shanghai - Brisbane 40ft / 40ft HC $2,465 $2,246 $2,094 $2,010 -11% -4% -41%
Shanghai - Melbourne 20ft $1,338 $1,310 $1,033 $1,111 -15% 8% -38%
Shanghai - Melbourne 40ft / 40ft HC $2,169 $2,178 $1,855 $1,930 -11% 4% -41%
Shanghai - Auckland 20ft $1,461 $1,545 $1,224 $1,159 -25% -5% -24%
Shanghai - Auckland 40ft / 40ft HC $2,519 $2,571 $2,240 $2,063 -20% -8% -22%
Jakarta - Melbourne 20ft $1,432 $1,298 $1,180 $1,268 -2% 7% -5%
Jakarta - Melbourne 40ft / 40ft HC $2,520 $2,341 $2,074 $2,216 -5% 7% -1%
Yokohama - Melbourne 20ft $2,432 $2,121 $1,883 $1,920 -9% 2% 2%
Yokohama - Melbourne 40ft / 40ft HC $4,029 $3,471 $2,994 $3,101 -11% 4% -4%
Yokohama - Auckland 20ft $1,913 $1,627 $1,835 $1,924 18% 5% 8%
Yokohama - Auckland 40ft / 40ft HC $3,506 $2,831 $3,299 $3,414 21% 3% 6%
Busan - Melbourne 20ft $1,579 $1,329 $1,110 $991 -25% -11% -30%
Busan - Melbourne 40ft / 40ft HC $2,900 $2,384 $2,051 $1,924 -19% -6% -26%
Auckland - Shanghai 20ft $954 $904 $1,099 $978 8% -11% 7%
Auckland - Shanghai 40ft / 40ft HC $1,421 $1,313 $1,574 $1,335 2% -15% 1%
Auckland - Jakarta 20ft $1,475 $1,476 $1,328 $1,446 -2% 9% 6%
Auckland - Jakarta 40ft / 40ft HC $2,126 $2,128 $1,771 $2,033 -4% 15% -1%
Auckland - Yokohama 20ft $1,214 $1,328 $1,317 $1,288 -3% -2% 3%
Auckland - Yokohama 40ft / 40ft HC $1,825 $2,112 $2,042 $1,642 -22% -20% -6%
Auckland - Tianjin 20ft $889 $929 $1,061 $996 7% -6% -4%
Auckland - Tianjin 40ft / 40ft HC $1,245 $1,281 $1,540 $1,411 10% -8% -3%
Auckland - Rotterdam 20ft $3,828 $3,558 $3,088 $3,097 -13% 0% -16%
Auckland - Rotterdam 40ft / 40ft HC $5,703 $5,058 $4,478 $4,487 -11% 0% -15%
Auckland - Yantian 20ft $1,074 $1,027 $1,148 $1,042 1% -9% -6%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 39 June 2025


=== Page 40 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Auckland - Yantian 40ft / 40ft HC $1,524 $1,292 $1,426 $1,307 1% -8% -11%
Auckland - Bangkok 20ft $1,037 $1,247 $1,217 $1,073 -14% -12% -12%
Auckland - Bangkok 40ft / 40ft HC $1,396 $1,663 $1,482 $1,416 -15% -4% -20%
Auckland - New York 20ft $4,282 $4,654 $4,496 $4,458 -4% -1% -9%
Auckland - New York 40ft / 40ft HC $5,864 $5,770 $5,498 $4,958 -14% -10% -17%
Auckland - Los Angeles 20ft $2,280 $2,294 $2,256 $2,174 -5% -4% -11%
Auckland - Los Angeles 40ft / 40ft HC $2,917 $2,930 $2,838 $2,736 -7% -4% -15%
Auckland - Genoa 20ft $3,836 $3,556 $3,050 $3,058 -14% 0% -16%
Auckland - Genoa 40ft / 40ft HC $5,726 $5,080 $4,517 $4,450 -12% -1% -16%
Tianjin - Brisbane 20ft $1,649 $1,635 $1,261 $1,339 -18% 6% -27%
Tianjin - Brisbane 40ft / 40ft HC $2,522 $2,619 $2,047 $2,185 -17% 7% -32%
Tianjin - Melbourne 20ft $1,596 $1,619 $1,151 $1,332 -18% 16% -29%
Tianjin - Melbourne 40ft / 40ft HC $2,498 $2,551 $1,838 $2,149 -16% 17% -37%
Tianjin - Auckland 20ft $1,237 $1,273 $1,191 $2,272 78% 91% 60%
Tianjin - Auckland 40ft / 40ft HC $2,022 $2,155 $2,050 $3,212 49% 57% 45%
Rotterdam - Melbourne 20ft $1,991 $1,780 $1,364 $1,318 -26% -3% -26%
Rotterdam - Melbourne 40ft / 40ft HC $2,656 $2,501 $2,027 $2,044 -18% 1% -23%
Rotterdam - Auckland 20ft $1,902 $2,225 $1,675 $1,778 -20% 6% -8%
Rotterdam - Auckland 40ft / 40ft HC $2,797 $3,092 $2,326 $2,535 -18% 9% -19%
Singapore - Melbourne 20ft $1,398 $1,182 $1,020 $815 -31% -20% -27%
Singapore - Melbourne 40ft / 40ft HC $2,356 $2,017 $1,748 $1,456 -28% -17% -20%
Yantian - Brisbane 20ft $1,586 $1,572 $1,368 $1,168 -26% -15% -35%
Yantian - Brisbane 40ft / 40ft HC $2,420 $2,500 $2,275 $2,119 -15% -7% -35%
Yantian - Auckland 20ft $1,422 $1,505 $1,085 $1,140 -24% 5% -22%
Yantian - Auckland 40ft / 40ft HC $2,504 $2,706 $1,991 $2,043 -25% 3% -23%
Felixstowe - Melbourne 20ft $2,264 $2,365 $2,251 $1,936 -18% -14% -3%
Felixstowe - Melbourne 40ft / 40ft HC $3,033 $3,072 $2,803 $2,698 -12% -4% 1%
New York - Melbourne 20ft $2,713 $2,708 $2,496 $2,299 -15% -8% -15%
New York - Melbourne 40ft / 40ft HC $3,950 $3,999 $3,667 $3,348 -16% -9% -21%
New York - Auckland 20ft $3,077 $2,644 $2,460 $2,309 -13% -6% -13%
New York - Auckland 40ft / 40ft HC $4,332 $3,851 $3,522 $3,277 -15% -7% -25%
Houston - Melbourne 20ft $2,796 $2,934 $2,686 $2,307 -21% -14% -30%
Houston - Melbourne 40ft / 40ft HC $3,641 $3,843 $3,406 $2,891 -25% -15% -36%
Chicago via LA-LB - Melbourne 20ft $3,102 $2,898 $2,926 $3,119 8% 7% -8%
Chicago via LA-LB - Melbourne 40ft / 40ft HC $4,058 $3,909 $4,019 $4,164 7% 4% -5%
Memphis via Savannah - Melbourne 20ft $3,233 $3,031 $2,821 $2,848 -6% 1% -2%
Memphis via Savannah - Melbourne 40ft / 40ft HC $4,476 $4,140 $4,246 $4,077 -2% -4% -4%
Los Angeles - Melbourne 20ft $2,322 $2,282 $2,198 $1,992 -13% -9% -20%
Los Angeles - Melbourne 40ft / 40ft HC $3,309 $3,245 $3,106 $2,789 -14% -10% -21%
Los Angeles - Auckland 20ft $2,424 $2,185 $2,034 $2,013 -8% -1% -32%
Los Angeles - Auckland 40ft / 40ft HC $3,396 $3,224 $2,888 $2,827 -12% -2% -30%
Genoa - Melbourne 20ft $1,900 $1,954 $1,790 $1,835 -6% 3% -0%
Genoa - Melbourne 40ft / 40ft HC $3,296 $3,331 $2,771 $2,908 -13% 5% -11%
Genoa - Auckland 20ft $2,527 $2,574 $2,290 $2,242 -13% -2% 12%
Genoa - Auckland 40ft / 40ft HC $3,997 $4,021 $3,314 $3,262 -19% -2% 2%
Brisbane - Auckland 20ft $1,144 - - $977 - - -30%
Brisbane - Auckland 40ft / 40ft HC $1,432 - - $1,447 - - -30%
Melbourne - Auckland 20ft $1,027 $1,110 $1,158 $1,082 -3% -7% -19%
Melbourne - Auckland 40ft / 40ft HC $1,343 $1,422 $1,477 $1,372 -4% -7% -34%
Melbourne - Ho Chi Minh City 20ft $1,225 $1,110 $955 $1,007 -9% 5% 14%
Melbourne - Ho Chi Minh City 40ft / 40ft HC $1,543 $1,499 $1,254 $1,315 -12% 5% 13%
Chennai - Melbourne 20ft $1,647 $1,645 $1,685 $1,635 -1% -3% 36%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 40 June 2025


=== Page 41 ===

Container Freight Rate | Insight
% change
Apr 25May 25Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun - Jun - Jun
25 25 25
Chennai - Melbourne 40ft / 40ft HC $2,962 $2,875 $2,752 $2,714 -6% -1% 37%
Jawaharlal Nehru Port - Melbourne 20ft $1,636 $1,623 $1,526 $1,297 -20% -15% 2%
Jawaharlal Nehru Port - Melbourne 40ft / 40ft HC $2,949 $2,795 $2,673 $2,272 -19% -15% 8%
Ho Chi Minh City - Melbourne 20ft $1,313 $1,278 $1,185 $1,171 -8% -1% -2%
Ho Chi Minh City - Melbourne 40ft / 40ft HC $2,309 $2,144 $2,039 $1,707 -20% -16% -15%
Click here for the full listings at www.drewry.co.uk
© Drewry Supply Chain Advisors 41 June 2025


=== Page 42 ===

INTRA EUROPE INDEX (US$/40FT)
Intra-Europe rates to Intra Europe Index (US$/40ft)
$1,300
remain flat
The Intra-European Index, which tracks freight rates on
$1,200
eight major European shipping routes, rose in June after
months of stability, increasing about 17% to $1,287.
$1,100
Drewry expects rates to remain steady in July. The index
was 2.4% higher than in June 2024 amid massive
congestion at European ports.
$1,000
I
A
n
n t
t
w
h
e
e
r p
M e
se
d
a
it
p
e
o
rr
r
a
ts
n e
h
a
a
n
s
,
i
c
n
o
te
n
n
g
s
e
i
s
fi
t
e
io
d
n
d
a
u
t
e
t
t
h
o
e
d
R
e
o
la
tt
y
e
s
r d
in
a m
o c
a
e
n
a
d
n Se
p- 2 4 Oct- 2 4 Nov- 2 4 Dec- 2 4
Ja
n- 2 5
Fe
b- 2 5 Mar- 2 5
A
pr- 2 5 May- 2 5
J u
n- 2 5
vessel arrivals, changes in shipping alliances, and limited
terminal capacities. These disruptions have decreased
operational efficiency and expanded waiting times, with Drewry Intra Europe Index (US$/40ft) Rate Index
the average waiting time currently at 90 hours for Antwerp History
and 76 hours for Rotterdam.
Sep-24 $1,130
Several major routes experienced significant rate hikes in Oct-24 $1,138 % change Sep 24 - Oct 24 1%
June. For instance, rates from Felixstowe to Port Said rose Nov-24 $1,117 % change Oct 24 - Nov 24 -2%
28% to $1,890 for a 40-ft container, and those from Port
Dec-24 $1,154 % change Nov 24 - Dec 24 3%
Said to Genoa spiked 18% to $888 for a 40-ft container.
Jan-25 $1,092 % change Dec 24 - Jan 25 -5%
Feb-25 $1,054 % change Jan 25 - Feb 25 -4%
Mar-25 $1,105 % change Feb 25 - Mar 25 5%
Apr-25 $1,113 % change Mar 25 - Apr 25 1%
May-25 $1,096 % change Apr 25 - May 25 -2%
Jun-25 $1,287 % change May 25 - Jun 25 17%
Intra Europe Index (US$/40ft)
(Rates on additional lanes are available via “Search rates” function on Container Freight Portal)
% change
Apr 25 May Jun 24
Port/region pairs Container Mar 25 Apr 25 May 25 Jun 25 - Jun 25 - - Jun
25 Jun 25 25
Felixstowe - Istanbul 20ft $818 $806 $708 $916 14% 29% 19%
Felixstowe - Istanbul 40ft / 40ft HC $998 $958 $856 $1,011 6% 18% 19%
Istanbul - Felixstowe 20ft $489 $480 $658 $1,166 143% 77% -3%
Istanbul - Felixstowe 40ft / 40ft HC $539 $480 $700 $1,242 159% 77% 4%
Felixstowe - Port Said 20ft $1,080 $1,109 $1,088 $1,286 16% 18% 46%
Felixstowe - Port Said 40ft / 40ft HC $1,683 $1,578 $1,475 $1,890 20% 28% 63%
Genoa - Istanbul 20ft $784 $823 $821 $738 -10% -10% -18%
Genoa - Istanbul 40ft / 40ft HC $1,035 $1,101 $1,039 $1,042 -5% 0% -9%
Genoa - Port Said 20ft $973 $1,023 $1,078 $1,045 2% -3% 12%
Genoa - Port Said 40ft / 40ft HC $1,611 $1,622 $1,615 $1,662 2% 3% 12%
Istanbul - Genoa 20ft $778 $818 $690 $788 -4% 14% -31%
Istanbul - Genoa 40ft / 40ft HC $1,040 $1,104 $978 $1,038 -6% 6% -34%
Port Said - Genoa 20ft $724 $677 $503 $590 -13% 17% -19%
Port Said - Genoa 40ft / 40ft HC $802 $794 $750 $888 12% 18% -9%
Rotterdam - Port Said 20ft $804 $1,028 $1,034 $1,126 10% 9% -3%
Rotterdam - Port Said 40ft / 40ft HC $1,135 $1,268 $1,356 $1,526 20% 13% -9%
© Drewry Supply Chain Advisors 42 June 2025


=== Page 43 ===

World Container Index
World Container Index ( US $/40ft )
World Container Index Week 23 Week 24 Week 25 Week 26 Weekly Trend
Composite Index $3,527 $3,543 $3,279 $2,983 -9 %
Shanghai - Rotterdam $2,845 $2,837 $3,171 $3,204 1 %
New York - Rotterdam $821 $815 $833 $826 -1 %
Rotterdam - Shanghai $509 $512 $517 $515 -0 %
Shanghai - Genoa $4,068 $4,054 $4,075 $4,100 1 %
Shanghai - Los Angeles $5,876 $5,914 $4,702 $3,741 -20 %
Los Angeles - Shanghai $716 $717 $718 $717 -0 %
Shanghai - New York $7,164 $7,286 $6,584 $5,703 -13 %
Rotterdam - New York $1,977 $1,982 $1,982 $1,982 0 %
Rate history
Shanghai - Rotterdam Composite Index
$3,500 $4,000
$3,000 $3,500
$2,500 $3,000
$2,000 $2,500
$1,500 $2,000
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
Rotterdam - Shanghai New York - Rotterdam
$525 $850
$840
$500
$830
$475
$820
$450 $810
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
© Drewry Supply Chain Advisors 43 June 2025


=== Page 44 ===

Shanghai - Los Angeles Shanghai - Genoa
$8,000 $4,500
$4,000
$6,000
$3,500
$4,000
$3,000
$2,000 $2,500
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
Shanghai - New York Los Angeles - Shanghai
$8,000 $720
$710
$6,000
$700
$4,000
$690
$2,000 $680
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
Rotterdam - New York
$2,200
$2,100
$2,000
$1,900
5 5 5 5 5 5 5 5 5 5 5 5 5
2 2 2 2 2 2 2 2 2 2 2 2 2
0 3- A
pr-
1 0- A
pr-
1 7- A
pr-
2 4- A
pr
0
-
1-
May
0
-
8-
May
1
-
5-
May
2
-
2-
May
2
-
9-
May-
0 5-J u
n-
1 2-J u
n-
1 9-J u
n-
2 6-J u
n-
© Drewry Supply Chain Advisors 44 June 2025


=== Page 45 ===

[No text found]
"""
SCFI_INDEX_URL = """ 
=== Page 1 ===

7/9/25, 10:22 PM Shanghai Shipping Exchange
Adobe Flash Player is no longer supported
Home About us Freight Indices Ship Trading Freight Rate Filing Member Services
Freight Indices
Introduction
User:
About Indices
Please input the period: (YYYY-MM-DD) 2025-07-09 Username: APPCN
FAQ
Contract Template
Indices
CCFI Shanghai Containerized Freight Index Contract Template
SSCCFFII
Previous Index Current Index Compare With
Description Unit Weighting
SCFIS 2025-06-27 2025-07-04 Last Week
CBFI Comprehensive Index 1861.51 1763.49 -98.02
CBCFI Europe (Base port) USD/TEU 20.0% 2030 2101 72
Mediterranean (Base port) USD/TEU 10.0% 2985 2869 -116
CBOFI
USWC (Base port) USD/FEU 20.0% 2578 2089 -490
CBGFI
USEC (Base port) USD/FEU 7.5% 4717 4124 -593
CDFI
Persian Gulf and Red Sea (Dubai) USD/TEU 7.5% 2060 1916 -144
FDI Australia/New Zealand (Melbourne) USD/TEU 5.0% 836 853 18
CTFI East/West Africa (Lagos) USD/TEU 2.5% 4526 4500 -26
South Africa (Durban) USD/TEU 2.5% 2641 2653 13
CSI
South America (Santos) USD/TEU 5.0% 6220 6374 154
CICFI
West Japan (Base port) USD/TEU 5.0% 312 312
SEAFI
East Japan (Base port) USD/TEU 5.0% 321 321
SRFTI Southeast Asia (Singapore) USD/TEU 7.5% 456 453 -3
BRSTI Korea (Pusan) USD/TEU 2.5% 136 136
Central/South America West Coast(Manzanillo) USD/TEU 0.0% 2346 2180 -166
BRTVI
East Africa(Mombasa) USD/TEU 0.0% 2583 2642 59
BRCVI
For any inquiry or purchase issue, please contact:
Mrs. Chen: 008621-65151166#2376 , ssebu_editor05@sse.net.cn
SRFI
Mr. Jiang: 008621-65151166#2356 , jiangt@sse.net.cn
GCSPI Issued by SSE
MTSR
CASR
PCSR
TWFI
CCRI
Report
Subscription
Bulletin
CFSA
© 2001-2025 Shanghai Shipping Exchange All Rights Reserved. Copyright Declaration Contact us
Shanghai ICP B2-20050110-1
https://en.sse.net.cn/indices/scfinew.jsp 1/1
"""

def get_model():
    """Menginisialisasi dan mengembalikan model Gemini."""
    # Menggunakan model yang mendukung pemanggilan fungsi (tool calling) dengan baik
    
    api_key = os.getenv("QWEN_API_KEY")
    api_base = os.getenv("QWEN_BASE_URL")
    model = os.getenv("QWEN_MODEL")
    return ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base=api_base,
        model_name=model,
        temperature=0.7
    )