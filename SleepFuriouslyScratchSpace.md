## add an n+7 module ##
Along these lines: http://www.spoonbill.org/n+7/

## fuzz word choice from input text by picking wrong synonyms... ##
Get a bilingual dictionary, look up source word, then get target word and pick a random source-language word. (maybe the original source word, maybe not.)

Could also use translation tables or phrase tables.

## use soundex or metaphone for rhyming, when a word's not in the pronunciation dictionary ##
Schwern has an implementation of some pronunciation algorithms in Perl:

http://search.cpan.org/~mschwern/Text-Metaphone-20081017/Metaphone.pm

## sleep furiously wants to become a webapp ##

## Introduction ##
TEB was and is my long-running electronic poetry project, originally for a class and written in Common Lisp on top of an inference engine. I should dust it off and make it awesome. At one point, I spoke with Jon Trowbridge from the Gnoetry project, and he seemed both interested in working on poetry and very busy with work. Does TEB want to use/be part of/merge with gnoetry?

Word to the gnoet: [Gnoetry is still going](http://gnoetrydaily.wordpress.com/), as of February 2010.

What TEB really really wants is to use NLTK (and probably be made of Python). Related: That horoscope remixer thing that never quite worked right.

## fake microblogging? ##
What if there was a fake microblogging service that never lets on that it's just snagging random chunks of text from user-generated content sites (people's tweets, blogs, comments (oh mans, youtube)), maybe remixing them slightly, and passing them off as tweets for fictional users? Bonus points for making it pretend that you can sign up for an account, but mysteriously diverting you away from where you can register. Authenticity/verisimilitude bonus points for keeping content persistently, serving it up as feeds.