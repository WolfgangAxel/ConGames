#Example Rules

Because Jeopardy is not originally intended for groups of people, the rules have to be modified. This is the ruleset I have used in the past when hosting a game, and it worked well for me. One note: this ruleset was played with [Dallin Lauritzen's JavaJeopardy](http://sourceforge.net/projects/dlauritz-javjeo/), so certain features (i.e. the Final Jeopardy round) are not yet implemented into Python Jeopardy (as of 6/28/16).


*  Number of teams: 4
*  Number of players per team: 3
*  Number of rounds: 3 (single-elimination)
*  Approximate round length: ~30 minutes
*  Total game length: ~1 hr 30 min
*  Points for questions: [100,200,300,400,500]
*  Rules:
  *  Basic: Teams will take turns selecting questions. The selecting team will get to guess first. After the question has been read, 20 seconds will be given for the selecting team to answer. If they get the question correct, they receive full points for that question. If they get it wrong, that many points are deducted from their score. When all questions have been answered, the round is over and the team with the highest score will advance to the final match. The final match will be a Double Jeopardy round and end with a Final Jeopardy question after the board is cleared of questions. If the final match will not be able to finish in time, the Final Jeopardy question will be asked before the board is cleared instead. Teams will wager the points they have earned through both of their rounds when shown the category. After the wagers are recorded, the question will be read, and the teams will be given one minute to converse with each other. After time runs out, teams will be asked to give their responses. If they give a correct response, their wager will be added to their score. If they give an incorrect response, their wager will be subtracted from their score. The team with the highest score at the end of the final round will be proclaimed the winners.
  *  Additional:
    *  Stealing: If the selecting team answers incorrectly, the other team has the **choice** to attempt to steal. If they choose to steal, they will get ½ points for a right answer or be deducted full points for a wrong answer, due to it being their choice to steal.
    *  Two-part questions: If a question or category has a two-part answer, full points will be awarded only if both answers are correctly given. If a team gets only one answer correct, then no points are deducted nor gained. If they get neither answer correct, they will be deducted full points. 
      *  Stealing on two-part questions will only be allowed if the first team got both answers incorrect.
    *  Bonus Answer: If a question has a bonus answer, the team that correctly answers the question has the chance to score bonus points equal to half of the smallest question value if they give the extra information asked (i.e. if using the [100,200,300,400,500] point array, bonus points yield 50 points; in the Double Jeopardy round, 100 points would be awarded).
