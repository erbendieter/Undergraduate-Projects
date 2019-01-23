library(readr)
library(dplyr)
library(stringr)
library(tidytext)
library(dummies)
if (!require("caret")) {
  install.packages("caret")
  library(caret)
}
if (!require("e1071")) {
  install.packages("e1071")
  library(e1071)
}

movies = read.csv('movie_metadata.csv',stringsAsFactors = FALSE)
og = movies

# Since the dataset is relatively large, and the number of NA's is less than 400
# for each column, I will delete all rows with a NA. This still gives us 3801 obs
# which I believe are enough for this exercise
movies = movies[complete.cases(movies), ]

# I am adding an index at the beginning in case I want to look at specific
# movie names later
movies = cbind(ID = seq.int(nrow(movies)), movies)
movie_names = subset(movies, select = c(ID, movie_title))


# Here I will try to get a sentiment score on the plot keywords to see if this helps
plot_words = subset(movies, select = c(ID, plot_keywords))

key_tokens <- plot_words %>%
  unnest_tokens(word, plot_keywords) %>%
  filter(!word %in% stop_words$word,
         str_detect(word, "^[a-z']+$"))

AFINN <- sentiments %>%
  filter(lexicon == "AFINN") %>%
  select(word, afinn_score = score)

key_sentiment <- key_tokens %>%
  inner_join(AFINN, by = "word") %>%
  group_by(ID) %>%
  summarize(sentiment = mean(afinn_score))

sent <- merge(movies, key_sentiment, all = TRUE)
sent[is.na(sent)] <- 0

# I will delete certain variables that are not available before a movie is released.
# For example, the number of criticts reviews. This is not the dependent variable
# and not available for new released movies.
clean = subset(sent, select = -c(color,director_name,num_critic_for_reviews,
                                   actor_2_name,actor_1_name,movie_title,num_voted_users,
                                   actor_3_name,movie_imdb_link,title_year,imdb_score,
                                   num_user_for_reviews,plot_keywords,genres,
                                 director_facebook_likes,cast_total_facebook_likes))

# I decided to get rid of the genre column because it has 753 different values.
# Many movies have multiple genres, and they are listed in alphabetical order
# so I can't just get the first value

# We can see here that 3626/3801 movies are in English, so I will just have a 
# binary with 1 being English and 0 being other movies.
# Same with country (3005/3801 are from the USA)
table(clean$language)

clean$language[clean$language %in% "English"] <- 1
'%!in%' <- function(x,y)!('%in%'(x,y))
clean$language[clean$language %!in% 1] <- 0
clean$country[clean$country %in% "USA"] <- 1
clean$country[clean$country %!in% 1] <- 0

clean = transform(clean, language = as.numeric(language))
clean = transform(clean, country = as.numeric(country))

# The rest of the categorical variables will just be dummies, and the model
# will get rid of the insignificant ones.
clean <- dummy.data.frame(clean, sep = ".")
clean$profit <- clean$gross - clean$budget

# I created a new variable that is basically a multiplier of the budget.
# I noticed that the 3rd quartile is 2.239. Therefore, I decided to call 
# a movie a "commercial succes" if it can at least duplicate its budget 
# with its gross income.

clean$success <- clean$gross / clean$budget
clean$success[clean$success < 2] <- 0
clean$success[clean$success >= 2] <- 1

# Our data is clean and ready to be analyzed now!
# I decided to go with a SVM that will label a movie as a "commercial success"
# I chose an SVM because it is highly accurate and we only have two classes
# for the dependent variable of success.

#  I got most of this code from the SVM Titanic example in class
svm.trainers = clean
svm.trainers <- svm.trainers[ -c(1, 5, 9:16, 20:21, 27) ]
svm.trainers$success=as.factor(svm.trainers$success)
names(svm.trainers)[7]<-"PG"
names(svm.trainers)[8]<-"PG13"
names(svm.trainers)[9]<-"PR"
svm.testers = read.csv('test.csv',stringsAsFactors = FALSE)
svm.testers = svm.testers[c(-1)]
samp_size <- floor(0.70 * nrow(svm.trainers))
set.seed(123)
train_ind <- sample(seq_len(nrow(svm.trainers)), size = samp_size)
svm.train <- svm.trainers[train_ind, ]
svm.test <- svm.trainers[-train_ind, ]

#  Create the SVM model and view prediction results
svm.model <- svm(success ~ ., svm.train, kernel="polynomial",cost=0.01,scale=TRUE,degree=3,gamma=1)
summary(svm.model)
svm.accuracy<-predict(svm.model,svm.test,type="class")
table(predict(svm.model), svm.test, dnn=c("Prediction", "Actual")) 
confusionMatrix(data = svm.accuracy,reference = svm.test$success)

#  Create a prediction of the test data and save for plotting later
svm.predict = predict(svm.model,svm.testers)
