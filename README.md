# CrazyManipulator

Found a way to get info for Crazy Time spins. The main goal is to extract useful information and maybe make biased decisions for more certain profits.

IF this is possible and the results are good tha xusw.

The api link found in a random json is this: 

**https://api.casinoscores.com/svc-evolution-game-events/api/crazytime**

Which returns the last 10 draws.

With a bit reverse engineer you can get the latest draw with this: 

**https://api.casinoscores.com/svc-evolution-game-events/api/crazytime/latest?tableId=CrazyTime0000001**

A bit MORE pontikareika and you can get the draws for the last 72 hours with this link: 

**https://api.casinoscores.com/svc-evolution-game-events/api/crazytime?size=40000&duration=2000&page=2&tableId=CrazyTime0000001**

The accepted values for page is 0,1,2. Expect for 0,1 around 2000 draws and the last page around 800-1000 draws
