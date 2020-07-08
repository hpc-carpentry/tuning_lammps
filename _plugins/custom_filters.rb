# Declare module of your plugin under Jekyll module

module Jekyll::CustomFilter

  # Each method of the module creates a custom Jekyll filter

  def multiline_string_in_callout(input, levels_of_indent = 0)
    input.split("\n").map{ |line| "> " * levels_of_indent + line }.join("\n")
  end

end

Liquid::Template.register_filter(Jekyll::CustomFilter)

