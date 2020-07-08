# Declare module of your plugin under Jekyll module

module Jekyll::CustomFilter

  # Each method of the module creates a custom Jekyll filter

  def append_to_newline(input, append_string = '')
    input.to_s.strip.gsub(/\n/, "\n" + append_string.to_s)
  end

end

Liquid::Template.register_filter(Jekyll::CustomFilter)

