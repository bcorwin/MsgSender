##########################################################
### To use:                                            ###
### Go to http://ondras.zarovi.cz/sql/demo/            ###
### Click Save/Load                                    ###
### Paste the output.xml text                          ###
### Click Load XML                                     ###
### Move tables around so they're viewable readable    ###
##########################################################

library(stringr)
template <- paste(readLines("model_extractor_template.xml"), collapse="\n")

setwd("..")
setwd("Factz")
filename <- "models.py"

file <- readLines(filename)
# Remove lines
## Blank lines
file <- file[!grepl("^[[:blank:]]*$", file)]
## Import statments
file <- file[!grepl("(^FROM)|(^IMPORT)", file, ignore.case = TRUE)]
## Anything with more than one indent
file <- file[!grepl("^[[:space:]]{5,}", file)]
## Methods and other def
file <- file[!grepl("^[[:space:]]*DEF", file, ignore.case = TRUE)]
## Classes within a model class
file <- file[!grepl("^[[:space:]]{4,}CLASS", file, ignore.case = TRUE)]
## Lines that are only comments
file <- file[!grepl("^[[:space:]]*#", file, ignore.case = TRUE)]

# Extract information
## Class name
reg <- "(?i)(^CLASS )(.*)(\\(models\\..*)"
classes <- ifelse(grepl(reg, file),
                  gsub(reg, "\\2", file), NA)

## Variable name, info, field type
reg <- "(?i)([[:space:]]{4})([^[:space:]]*)([[:space:]]*=[[:space:]]*models\\.)([[:alnum:]]+)(\\(.*)"
vars <- ifelse(is.na(classes) & grepl(reg, file),
               gsub(reg, "\\2", file),NA)
info <- ifelse(is.na(classes) & grepl(reg, file),
               gsub(reg, "\\5", file),NA)
types <- ifelse(is.na(classes) & grepl(reg, file),
                gsub(reg, "\\4", file),NA)
types <- gsub("Field", "", types)



# Get list of parameters
parms <- unlist(str_match_all(info, "[[:alnum:]_]*[[:space:]]*="))
parms <- sort(unique(gsub("=|[[:space:]]*", "", parms)))

# Put it all together
file_df <- data.frame(line=file,
                      class=classes,
                      var=vars,
                      type=types,
                      info=info,
                      stringsAsFactors=FALSE)

# Extract parmeter values
for(name in parms){
  reg = paste0("(?i)\\(.*",name,"[[:space:]]*=[[:space:]]*([[:alnum:]_.]*(\\[.*\\]|\\(.*\\)){0,1}).*\\)")
  file_df[name] <- ifelse(grepl(reg, file_df$info),
                          gsub(reg, "\\1", file_df$info), NA)
}

# Append class and remove class rows
curr_class <- NA
for(rnum in seq(nrow(file_df))) {
  row <- file_df[rnum,]
  if(!is.na(row$class)){
    curr_class <- row$class
  } else {
    file_df[rnum, "class"] <- curr_class
  }
}
file_df <- file_df[!is.na(file_df$var), ]

# Get fk table name
file_df$fk_table <- ifelse(file_df$type == "ForeignKey",
                           gsub("\\(([[:alnum:]_]*).*", "\\1", file_df$info),
                           NA)

# Build XML file
loc <- c(1,1)
classes <- na.omit(unique(classes))
output <- NULL
for(curr_class in classes) {
  curr_df <- file_df[file_df$class==curr_class,]
  
  table <- paste0('<table x="', loc[1], '" y="', loc[2], '" name="', curr_class, '">')
  loc <- loc+10
  
  curr_var <- c('<row name="id" null="1" autoincrement="1">',
                '<datatype>INTEGER</datatype>',
                '<default>NULL</default></row>')
  
  table <- c(table, curr_var)
  for(rnum in seq(nrow(curr_df))) {
    curr_row <- curr_df[rnum,]
    #First line of the row
    curr_var <- paste0('<row name="', curr_row$var, '" ')
    if(identical(curr_row$null, "True")) {
      curr_var <- paste0(curr_var, 'null="1" ')
    } else{
      curr_var <- paste0(curr_var, 'null="0" ')
    }
    curr_var <- paste0(curr_var, 'autoincrement="0">')
    
    #Variable type
    if(curr_row$type %in% c("Integer", "PositiveInteger")) {
      curr_var <- c(curr_var, '<datatype>INTEGER</datatype>')
    } else if(curr_row$type %in% c("Char")) {
      curr_var <- c(curr_var, '<datatype>CHAR</datatype>')
    } else if(curr_row$type %in% c("DateTime")) {
      curr_var <- c(curr_var, '<datatype>DATETIME</datatype>')
    } else if(curr_row$type %in% c("Date")) {
      curr_var <- c(curr_var, '<datatype>DATE</datatype>')
    } else if(curr_row$type %in% c("Time")) {
      curr_var <- c(curr_var, '<datatype>TIME</datatype>')
    } else if(curr_row$type %in% c("Boolean")) {
      curr_var <- c(curr_var, '<datatype>bit</datatype>')
    } else if(curr_row$type %in% c("ForeignKey")) {
      curr_var <- c(curr_var, '<datatype>INTEGER</datatype>')
      curr_var <- c(curr_var, paste0('<relation table="', curr_row$fk_table , '" row="id" />'))
    } else {
      stop("Unknown variable type: ", curr_row$type)
    }
    
    #Default
    if(!is.na(curr_row$default)) {
      curr_var <- c(curr_var, paste0('<default>', curr_row$default,'</default>'))
    }
    curr_var <- c(curr_var, "</row>")
    table <- c(table, curr_var)
  }
  table <- c(table, '<key type="PRIMARY" name="">',
             '<part>id</part>',
             '</key></table>')
  output <- c(output, table)
}
output <- c(template, output, "</sql>")

setwd("..")
setwd("Other")
cat(output, file="output.xml", sep="\n")